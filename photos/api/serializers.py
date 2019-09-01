from django.db.models import Q
from django.urls import reverse

from rest_framework import serializers

from photos.api.fields import (
    GroupField, NullableAlbumField, PhotoHashField, TagField, UserField)
from photos.models import Album, Photo

from collections import OrderedDict


class AlbumSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)

    tags = TagField(many=True, allow_empty=True, queryset=Q())
    users = UserField(many=True, allow_empty=True, queryset=Q())
    groups = GroupField(many=True, allow_empty=True, queryset=Q())
    parent = NullableAlbumField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'path',
            'place', 'location', 'description', 'tags',
            'start', 'end',
            'thumbnail_size',
            'access_level', 'access_code', 'users', 'groups',
            'parent',
        )


class AlbumCoverSerializer(serializers.ModelSerializer):
    cover = PhotoHashField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = ('cover',)


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
