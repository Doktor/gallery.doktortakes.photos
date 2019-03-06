from typing import Optional

from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

import datetime
import pytz
from io import BytesIO

from photos.api.utils import APIError, APIView, api_wrapper
from photos.models.photo import Photo
from photos.models.utils import generate_md5_hash, CHUNK_SIZE
from photos.utils import get_album_by_path
from photos.settings import ITEMS_PER_PAGE


def get_photo(request: HttpRequest, md5: str, validate_path: Optional[str] = None) -> Photo:
    if validate_path is not None:
        album = get_album_by_path(validate_path)
        photo = get_object_or_404(Photo, md5=md5, album=album)
    else:
        photo = get_object_or_404(Photo, md5=md5)

    if not photo.sidecar_exists:
        raise Http404

    access, status = photo.check_access(request)

    if not access:
        raise Http404

    if status is not None:
        messages.warning(request, status.message)

    return photo


def get_photo_from_request(request: HttpRequest, path: str) -> Photo:
    try:
        md5 = request.GET.get('md5')
    except KeyError:
        raise APIError("The parameter 'md5' is required.")

    try:
        photo = get_photo(request, md5, validate_path=path)
    except Http404:
        raise APIError("Photo does not exist.", status=404)

    return photo


class PhotoView(APIView):
    def get(self, request: HttpRequest, path: str) -> JsonResponse:
        photo = get_photo_from_request(request, path)

        return JsonResponse(
            photo.serialize(
                admin=request.user.is_staff,
                password='password' in request.GET))

    def delete(self, request: HttpRequest, path: str) -> JsonResponse:
        if not request.user.is_staff:
            raise APIError("Not authorized", status=403)

        photo = get_photo_from_request(request, path)
        photo.delete()

        return JsonResponse({'message': "Photo deleted successfully."})


@api_wrapper
@require_POST
def upload_photo(request: HttpRequest, path: str) -> JsonResponse:
    if not request.user.is_staff:
        raise APIError("Not authorized", status=403)

    files = request.FILES.getlist('files')
    album = get_album_by_path(path)

    for file in files:
        p = Photo()
        p.album = album

        # Check if this image already exists
        md5 = generate_md5_hash(file)

        try:
            Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise APIError(f"Duplicate file: {md5}")

        p.md5 = md5

        filename = file.name

        try:
            original = Photo.objects.get(album=album, original_filename=filename)
        except Photo.DoesNotExist:
            pass
        else:
            original.delete()

        data = BytesIO()
        data.name = filename

        p.original_filename = filename

        for chunk in file.chunks(chunk_size=CHUNK_SIZE):
            data.write(chunk)

        # Expires after 24 hours
        cache.set(md5, data, 60 * 60 * 24)

        p.save()

    return JsonResponse({'success': True})


def date_query(start: str, end: str) -> Q:
    query = Q()

    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        start = start.replace(tzinfo=pytz.utc)
    except ValueError:
        start = False

    try:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = end.replace(tzinfo=pytz.utc)
    except ValueError:
        end = False

    if start and end:
        query &= Q(taken__gte=start, taken__lte=end)
    elif start or end:
        day = start or end
        day_end = day.replace(hour=23, minute=59, second=59)

        query &= Q(taken__gte=day, taken__lte=day_end)
    else:
        pass

    return query


def search_photos(request: HttpRequest) -> JsonResponse:
    params = request.GET
    query = Q(album__hidden=False)

    # Filtering: general

    fields = (
        ('name', 'album__name__icontains', None),
        ('location', 'album__location__icontains', None),
        ('width', 'width', int),
        ('height', 'height', int),
    )

    for key, field, f in fields:
        value = params.get(key, '')

        if value:
            if f is not None:
                value = f(value)

            query &= Q(**{field: value})

    rating = params.getlist('rating')
    if rating:
        subquery = Q()

        for value in rating:
            try:
                value = int(value)
            except ValueError:
                continue

            subquery |= Q(rating=value)

        query = query & subquery

    # Filtering: dates

    taken_start = params.get('taken-start', '')
    taken_end = params.get('taken-end', '')

    uploaded_start = params.get('uploaded-start', '')
    uploaded_end = params.get('uploaded-end', '')

    query &= date_query(taken_start, taken_end)
    query &= date_query(uploaded_start, uploaded_end)

    # Ordering

    order = params.get('order')

    if order not in ('taken', 'edited', 'uploaded'):
        order = 'taken'

    if params.get('direction') == 'new':
        order = f"-{order}"

    # Execute the query!

    photos = Photo.objects.filter(query).order_by(order)
    total = photos.count()

    try:
        page = int(params.get('page'))
    except (ValueError, KeyError):
        page = 1

    # Pagination

    first = ITEMS_PER_PAGE * (page - 1)
    last = first + ITEMS_PER_PAGE

    photos = photos[first:last]

    # Generate the response

    data = [photo.serialize(metadata=False) for photo in photos]

    response = {
        'photos': data,
        'count': total,
    }

    return JsonResponse(response)
