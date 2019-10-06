from django.db.models import Q

from rest_framework import serializers

from photos.api.fields import (
    TagField, UserField, GroupField, NullableAlbumField, PhotoHashField)
from photos.api.serializers import PhotoThumbnailSerializer
from photos.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)

    cover = PhotoThumbnailSerializer(read_only=True)

    tags = TagField(many=True, allow_empty=True, queryset=Q())
    users = UserField(many=True, allow_empty=True, queryset=Q())
    groups = GroupField(many=True, allow_empty=True, queryset=Q())
    parent = NullableAlbumField(allow_empty=True, allow_null=True, queryset=Q())

    url = serializers.CharField(read_only=True, source='get_absolute_url')
    edit_url = serializers.CharField(read_only=True, source='get_edit_url')
    admin_url = serializers.CharField(read_only=True, source='get_admin_url')

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'path',
            'place', 'location', 'description', 'tags',
            'start', 'end',
            'cover',
            'thumbnail_size',
            'access_level', 'access_code', 'users', 'groups',
            'parent',
            'url', 'edit_url', 'admin_url',
        )


class AlbumCoverSerializer(serializers.ModelSerializer):
    cover = PhotoHashField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = ('cover',)


class AlbumForListViewSerializer(serializers.ModelSerializer):
    cover = PhotoThumbnailSerializer(read_only=True)

    class Meta:
        model = Album
        fields = (
            'name', 'path',
            'place', 'location', 'description',
            'start', 'end',
            'cover',
            'access_level',
        )
        read_only_fields = fields
