from django.core.exceptions import ValidationError
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
    children = serializers.SerializerMethodField(read_only=True)

    url = serializers.CharField(read_only=True, source='get_absolute_url')
    admin_url = serializers.CharField(read_only=True, source='get_admin_url')

    @staticmethod
    def get_children(obj: Album):
        return ChildAlbumSerializer(obj.children, many=True).data

    def validate(self, data):
        if self.instance is not None:
            data['id'] = self.instance.id

        try:
            Album.validate_fields(data)
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.message)
        else:
            return data

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'path',
            'place', 'location', 'description', 'tags',
            'start', 'end',
            'cover',
            'display_image_size',
            'access_level', 'access_code', 'users', 'groups',
            'parent', 'children',
            'url', 'admin_url',
        )


class SimpleAlbumSerializer(serializers.ModelSerializer):
    cover = PhotoThumbnailSerializer(read_only=True)
    url = serializers.CharField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'path',
            'place', 'location', 'description',
            'start', 'end',
            'cover',
            'url',
        )
        read_only_fields = ('slug', 'path')


class ChildAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('name', 'path')


class AlbumCoverSerializer(serializers.ModelSerializer):
    cover = PhotoHashField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = ('cover',)
