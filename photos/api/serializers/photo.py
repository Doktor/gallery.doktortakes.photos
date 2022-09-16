from django.urls import reverse
from rest_framework import serializers

from photos.api.serializers.thumbnail import ThumbnailSerializer
from photos.models.photo.thumbnail import THUMBNAIL_DISPLAY, THUMBNAIL_SMALL_SQUARE
from photos.models import Photo

import itertools
from collections import OrderedDict


def serialize_thumbnail(thumbnail: "Thumbnail"):
    return ThumbnailSerializer(thumbnail).data


THUMBNAIL_TYPES = (
    # (property name, internal name)
    ("display", THUMBNAIL_DISPLAY),
    ("square", THUMBNAIL_SMALL_SQUARE),
)


class PhotoSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    # Links
    url = serializers.CharField(read_only=True, source='get_absolute_url')
    admin = serializers.SerializerMethodField(read_only=True, allow_null=True)

    # Metadata
    taken = serializers.DateTimeField(
        read_only=True, format="%A, %Y-%m-%d, %-I:%M:%S %p")
    index = serializers.IntegerField(
        read_only=True, allow_null=True, default=None)
    exif = serializers.DictField(read_only=True, source='get_exif')

    @staticmethod
    def get_images(obj: Photo) -> dict:
        temp = {}

        for key, group in itertools.groupby(obj.thumbnails.all(), lambda t: t.type):
            temp[key] = next(group)

        thumbnails = {
            name: serialize_thumbnail(temp[key]) if key in temp else None
            for (name, key) in THUMBNAIL_TYPES
        }

        if thumbnails["display"] is None:
            thumbnails["original"] = {
                "url": obj.original.url,
                "name": obj.original.name,
                "type": "original",
                "width": obj.width,
                "height": obj.height,
            }

        return thumbnails

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
            'images',
            'url', 'admin',
            'taken',
            'width', 'height', 'md5', 'index',
            'path', 'exif',
        )


class SimplePhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    square_thumbnail = serializers.ImageField(use_url=True)
    url = serializers.CharField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Photo
        fields = ('image', 'square_thumbnail', 'url')


class PhotoThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True, allow_null=True)

    @staticmethod
    def get_thumbnail(obj: Photo):
        thumbnail = obj.get_large_square_thumbnail()
        serializer = ThumbnailSerializer(thumbnail)
        return serializer.data

    class Meta:
        model = Photo
        fields = ('thumbnail',)
