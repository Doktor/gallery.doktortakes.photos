from django.db.models import Q
from django.urls import reverse

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models.album import Allow
from photos.models.photo import Photo
from photos.settings import ITEMS_PER_PAGE
from photos.utils import get_photo

import datetime
import pytz
from collections import OrderedDict
from http import HTTPStatus as Status


class PhotoDetail(APIView):
    @staticmethod
    def get(request: Request, md5: str) -> Response:
        photo = get_photo(md5, request)
        serializer = PhotoSerializer(photo)

        return Response(serializer.data)

    @staticmethod
    def delete(request: Request, md5: str) -> Response:
        if not request.user.is_staff:
            return Response(None, status=Status.FORBIDDEN)

        photo = get_photo(md5, request)
        photo.delete()

        return Response(status=Status.NO_CONTENT)


class PhotoSerializer(serializers.ModelSerializer):
    # Links
    image = serializers.ImageField(use_url=True)
    square_thumbnail = serializers.ImageField(use_url=True)
    url = serializers.CharField(read_only=True, source='get_absolute_url')
    download = serializers.CharField(read_only=True, source='get_download_url')
    admin = serializers.SerializerMethodField(read_only=True, allow_null=True)

    # Metadata
    taken = serializers.DateTimeField(
        read_only=True, format="%A, %Y-%m-%d, %-I:%M:%S %p")
    index = serializers.IntegerField(
        read_only=True, allow_null=True, default=None)
    exif = serializers.DictField(read_only=True, source='get_exif')

    def get_admin(self, obj: Photo):
        if self.context.get('is_staff', False):
            return reverse('admin:photos_photo_change', args=[obj.pk])
        else:
            return None

    def to_representation(self, instance: Photo) -> dict:
        instance.index = self.context.get('index', None)

        result = super().to_representation(instance)

        # Don't serialize null values
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = Photo
        fields = (
            'image', 'square_thumbnail', 'url', 'download', 'admin',
            'taken',
            'width', 'height', 'md5', 'index',
            'exif'
        )


class SimplePhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    square_thumbnail = serializers.ImageField(use_url=True)
    url = serializers.CharField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Photo
        fields = ('image', 'square_thumbnail', 'url')


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

    data = [SimplePhotoSerializer(photo).data for photo in photos]

    response = {
        'photos': data,
        'count': total,
    }

    return Response(response)
