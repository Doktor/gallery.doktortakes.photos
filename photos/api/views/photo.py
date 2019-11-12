from django.db.models import Q
from django.http import Http404

from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import PhotoSerializer, SimplePhotoSerializer
from photos.models import Photo
from photos.models.album import Allow
from photos.settings import ITEMS_PER_PAGE
from photos.utils import get_photo_for_user_or_404

import datetime
import pytz
from http import HTTPStatus as Status


class PhotoNotFound(exceptions.APIException):
    status_code = Status.NOT_FOUND

    def __init__(self):
        super().__init__("Photo not found.")


class PhotoDetail(APIView):
    @staticmethod
    def get_photo(request, md5) -> Photo:
        try:
            return get_photo_for_user_or_404(request, md5)
        except Http404:
            raise PhotoNotFound

    def get(self, request: Request, md5: str) -> Response:
        photo = self.get_photo(request, md5)
        serializer = PhotoSerializer(photo)

        return Response(serializer.data)

    def delete(self, request: Request, md5: str) -> Response:
        if not request.user.is_staff:
            raise exceptions.PermissionDenied("Not authorized.")

        photo = self.get_photo(request, md5)
        photo.delete()

        return Response(status=Status.NO_CONTENT)


@api_view()
def get_featured_photos(request: Request) -> Response:
    query = Q(album__access_level=Allow.PUBLIC, rating__gte=4, sidecar_exists=True)
    photos = Photo.objects.filter(query).order_by('-taken').select_related('album')

    serializer = PhotoSerializer(photos[:30], many=True)
    return Response({'photos': serializer.data})


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


@api_view()
def search_photos(request: Request) -> Response:
    params = request.query_params
    query = Q(album__access_level=Allow.PUBLIC)

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

    ratings = params.get('ratings', '').split(',')
    if ratings:
        subquery = Q()

        for value in ratings:
            try:
                value = int(value)
            except ValueError:
                continue

            subquery |= Q(rating=value)

        query = query & subquery

    # Filtering: dates

    taken_start = params.get('takenStart', '')
    taken_end = params.get('takenEnd', '')

    uploaded_start = params.get('uploadedStart', '')
    uploaded_end = params.get('uploadedEnd', '')

    query &= date_query(taken_start, taken_end)
    query &= date_query(uploaded_start, uploaded_end)

    # Ordering

    order = params.get('order')

    if order not in ('taken', 'edited', 'uploaded'):
        order = 'taken'

    if params.get('direction') == 'new':
        order = f"-{order}"

    # Execute the query

    photos = Photo.objects.filter(query).order_by(order).select_related('album')
    total = photos.count()

    # Pagination

    try:
        page = int(params.get('page'))
    except (ValueError, KeyError):
        page = 1

    per_page = int(params.get('itemsPerPage', 0)) or ITEMS_PER_PAGE

    first = per_page * (page - 1)
    last = first + per_page

    photos = photos[first:last]

    # Generate the response

    data = [PhotoSerializer(photo).data for photo in photos]

    response = {
        'photos': data,
        'count': total,
        'page': page,
    }

    return Response(response)
