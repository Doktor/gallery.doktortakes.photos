from rest_framework import serializers

from photos.api.serializers.taxon import TaxonSerializer
from photos.api.serializers.thumbnail import ThumbnailSerializer
from photos.models.photo.thumbnail import (
    THUMBNAIL_DISPLAY, THUMBNAIL_SMALL_SQUARE, THUMBNAIL_MEDIUM_SQUARE, THUMBNAIL_EXTRA_SMALL_SQUARE)
from photos.models import Photo

import itertools
from collections import OrderedDict


def serialize_thumbnail(thumbnail: "Thumbnail"):
    return ThumbnailSerializer(thumbnail).data


THUMBNAIL_TYPES = (
    # (property name, internal name)
    ("display", THUMBNAIL_DISPLAY),
    ("extraSmallSquare", THUMBNAIL_EXTRA_SMALL_SQUARE),
    ("square", THUMBNAIL_SMALL_SQUARE),
    ("mediumSquare", THUMBNAIL_MEDIUM_SQUARE),
)


def get_images(photo: Photo) -> dict:
    temp = {}

    for key, group in itertools.groupby(photo.thumbnails.all(), lambda t: t.type):
        temp[key] = next(group)

    thumbnails = {
        name: serialize_thumbnail(temp[key]) if key in temp else None
        for (name, key) in THUMBNAIL_TYPES
    }

    if thumbnails["display"] is None:
        thumbnails["original"] = {
            "url": photo.original.url,
            "name": photo.original.name,
            "type": "original",
            "width": photo.width,
            "height": photo.height,
        }

    return thumbnails


class PhotoSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    # Metadata
    taken = serializers.DateTimeField(
        read_only=True, format="%A, %Y-%m-%d, %-I:%M:%S %p")
    taken_date = serializers.DateTimeField(
        source="taken", read_only=True, format="%A, %B %-m, %Y")
    taken_time = serializers.DateTimeField(
        source="taken", read_only=True, format="%-I:%M:%S %p")
    index = serializers.IntegerField(
        read_only=True, allow_null=True, default=None)
    exif = serializers.DictField(read_only=True, source='get_exif')

    taxa = TaxonSerializer(many=True)

    @staticmethod
    def get_images(obj: Photo) -> dict:
        return get_images(obj)

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
            'taken', 'taken_date', 'taken_time',
            'width', 'height', 'md5', 'index',
            'path', 'exif',
            'taxa',
        )


class SimplePhotoSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_images(obj: Photo) -> dict:
        return get_images(obj)

    class Meta:
        model = Photo
        fields = ('images', 'md5', 'path')


class PhotoThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True, allow_null=True)

    @staticmethod
    def get_thumbnail(obj: Photo):
        thumbnail = obj.get_large_square_thumbnail()
        serializer = ThumbnailSerializer(thumbnail)
        return serializer.data

    class Meta:
        model = Photo
        fields = ('thumbnail', 'placeholder_color')
