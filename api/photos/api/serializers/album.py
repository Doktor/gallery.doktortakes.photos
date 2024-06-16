from django.core.exceptions import ValidationError
from django.db.models import Q

from rest_framework import serializers

from photos.api.fields import (
    TagField, UserField, GroupField, NullableAlbumField, PhotoHashField)
from photos.models import Album, License

from .license import LicenseSerializer
from .photo import PhotoThumbnailSerializer


class AlbumSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)

    license = LicenseSerializer(read_only=True)
    license_id = serializers.PrimaryKeyRelatedField(
        queryset=License.objects, write_only=True)

    cover = PhotoThumbnailSerializer(read_only=True)

    tags = TagField(many=True, allow_empty=True, queryset=Q())
    users = UserField(many=True, allow_empty=True, queryset=Q())
    groups = GroupField(many=True, allow_empty=True, queryset=Q())

    parent = NullableAlbumField(allow_empty=True, allow_null=True, queryset=Q())

    url = serializers.CharField(read_only=True, source='get_absolute_url')
    admin_url = serializers.CharField(read_only=True, source='get_admin_url')

    def create(self, validated_data):
        license = validated_data.pop('license_id')

        tags = validated_data.pop('tags')
        users = validated_data.pop('users')
        groups = validated_data.pop('groups')

        album = Album.objects.create(license=license, **validated_data)

        album.tags.set(tags)
        album.users.set(users)
        album.groups.set(groups)

        return album

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
            'license', 'license_id',
            'start', 'end',
            'cover',
            'access_level', 'access_code', 'users', 'groups',
            'parent',
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
            'access_level',
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
