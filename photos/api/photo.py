from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

import datetime
import pytz
from io import BytesIO

from photos.api.utils import (
    APIError, APIView, get_photo_from_request, api_wrapper)
from photos.models.photo import Photo
from photos.models.utils import generate_md5_hash, CHUNK_SIZE
from photos.settings import ITEMS_PER_PAGE
from photos.views import get_album_by_path, get_photo


def get_photo_by_hash(path, md5):
    try:
        return get_photo(path, md5)
    except Photo.DoesNotExist:
        raise APIError("The specified photo doesn't exist.", status=404)


class PhotoView(APIView):
    def get(self, request, path):
        photo = get_photo_from_request(request, path)

        if not photo.check_access(request):
            raise APIError("Photo does not exist.", status=404)

        return JsonResponse(photo.serialize(password='password' in request.GET))

    def delete(self, request, path):
        if not request.user.is_staff:
            raise APIError("Not authorized", status=403)

        photo = get_photo_from_request(request, path)
        photo.delete()
        return JsonResponse({'message': "Photo deleted successfully."})


def navigate(request, path, method):
    md5 = request.GET.get('md5', '')
    photo = get_photo_by_hash(path, md5)

    if not photo.check_access(request):
        raise APIError("Photo not found", status=404)

    try:
        nav = getattr(photo, method)(album=photo.album)
    except Photo.DoesNotExist:
        photos = Photo.objects.filter(album=photo.album)

        # At the oldest photo: return the newest
        if method == 'get_previous_by_taken':
            nav = photos.order_by('-taken')[0]

        # At the newest photo: return the oldest
        elif method == 'get_next_by_taken':
            nav = photos.order_by('taken')[0]

    return JsonResponse(nav.serialize())


@api_wrapper
@require_GET
def previous_photo(request, path):
    return navigate(request, path, 'get_previous_by_taken')


@api_wrapper
@require_GET
def next_photo(request, path):
    return navigate(request, path, 'get_next_by_taken')


def navigate_end(request, path, method):
    album = get_album_by_path(path)
    photos = Photo.objects.filter(album=album).order_by('taken')

    if not photos:
        raise APIError("There are no photos in this album.")

    photo = getattr(photos, method)()

    if not photo.check_access(request):
        raise APIError("Photo not found", status=404)

    return JsonResponse(photo.serialize())


@api_wrapper
@require_GET
def first_photo(request, path):
    return navigate_end(request, path, 'first')


@api_wrapper
@require_GET
def last_photo(request, path):
    return navigate_end(request, path, 'last')


@api_wrapper
@require_POST
def upload_photo(request, path):
    if not request.user.is_staff:
        raise APIError("Not authorized", status=403)

    files = request.FILES.getlist('files')

    for file in files:
        p = Photo()
        p.album = get_album_by_path(path)

        # Check if this image already exists
        md5 = generate_md5_hash(file)

        try:
            Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise APIError(f"Duplicate file: {md5}")

        p.md5 = md5

        data = BytesIO()
        data.name = file.name

        for chunk in file.chunks(chunk_size=CHUNK_SIZE):
            data.write(chunk)

        # Expires after 24 hours
        cache.set(md5, data, 60 * 60 * 24)

        p.save()

    return JsonResponse({'success': True})


def date_query(start, end):
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


def search_photos(request):
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

    data = [photo.serialize(metadata=False, filmstrip=False)
            for photo in photos]

    response = {
        'photos': data,
        'count': total,
    }

    return JsonResponse(response)
