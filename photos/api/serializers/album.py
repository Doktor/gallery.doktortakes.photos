from django.db.models import Q

from rest_framework import serializers

from photos.api.fields import (
    TagField, UserField, GroupField, NullableAlbumField, PhotoHashField)
from photos.models import Album


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
