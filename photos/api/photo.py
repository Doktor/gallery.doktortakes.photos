from django.core.cache import cache
from django.db.models import Q
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models.album import Allow
from photos.models.photo import Photo
from photos.models.utils import generate_md5_hash, CHUNK_SIZE
from photos.utils import get_album_by_path
from photos.settings import ITEMS_PER_PAGE

import datetime
import pytz
from collections import OrderedDict
from http import HTTPStatus as Status
from io import BytesIO
from typing import Optional


def get_photo(request: HttpRequest, md5: str, path: Optional[str] = None) -> Photo:
    if path is not None:
        try:
            album = get_album_by_path(path)
        except IndexError:
            raise Http404

        photo = get_object_or_404(Photo, md5=md5, album=album)
    else:
        photo = get_object_or_404(Photo, md5=md5)

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    return photo


class PhotoDetail(APIView):
    @staticmethod
    def get_photo(request: Request, md5: str) -> Photo:
        try:
            photo = get_photo(request, md5)
        except Http404:
            raise ValidationError("Photo does not exist.")

        return photo

    def get(self, request: Request, md5: str) -> Response:
        photo = self.get_photo(request, md5)
        serializer = PhotoSerializer(photo)

        return Response(serializer.data)

    def delete(self, request: Request, md5: str) -> Response:
        if not request.user.is_staff:
            return Response(None, status=Status.FORBIDDEN)

        photo = self.get_photo(request, md5)
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


@api_view
@require_POST
def upload_photo(request: Request, path: str) -> Response:
    if not request.user.is_staff:
        return Response(None, status=Status.FORBIDDEN)

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
            raise ValidationError(f"Duplicate file: {md5}")

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

    return Response({'success': True}, status=Status.OK)


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
