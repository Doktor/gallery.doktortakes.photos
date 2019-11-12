from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from photos.models import Photo, Tag, Album
from photos.utils import get_album_for_user_or_404

from http import HTTPStatus as Status
from typing import Optional

User = get_user_model()


class GroupField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Group:
        name = data.lower().strip().replace('group:', '').strip()

        try:
            group = Group.objects.get(name__iexact=name)
        except Group.DoesNotExist:
            raise ValidationError(f"Group '{name}' does not exist.", code=Status.BAD_REQUEST)
        else:
            return group

    def to_representation(self, value: Group) -> str:
        return value.name


class NullableAlbumField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Optional[Album]:
        return get_object_or_404(Album, path=data) if data else None

    def to_representation(self, value: Album) -> str:
        return value.path


class PhotoHashField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Photo:
        try:
            return Photo.objects.get(md5=data)
        except Photo.DoesNotExist:
            raise ValidationError(f"Photo '{data}' does not exist.", code=Status.BAD_REQUEST)

    def to_representation(self, value: Photo) -> str:
        return value.md5


class TagField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Tag:
        slug = slugify(data)

        if not slug:
            raise ValidationError("Tag name can't be empty.", code=Status.BAD_REQUEST)

        try:
            tag = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(slug=slug)

        return tag

    def to_representation(self, value: Tag) -> str:
        return value.slug


class UserField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> User:
        name = data.lower().strip()

        try:
            user = User.objects.get(username__iexact=name)
        except User.DoesNotExist:
            raise ValidationError(f"User '{name}' does not exist.", code=Status.BAD_REQUEST)
        else:
            return user

    def to_representation(self, value: User) -> str:
        return value.username.capitalize()
