from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from photos.models import Photo, Tag, Album
from photos.utils import get_album

from typing import Optional

User = get_user_model()


class AlbumField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Optional[Album]:
        return get_album(data) if data else None

    def to_representation(self, value: Album) -> str:
        return value.get_path()


class GroupField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Group:
        name = data.lower().strip().replace('group:', '').strip()

        try:
            group = Group.objects.get(name__iexact=name)
        except Group.DoesNotExist:
            raise ValidationError(f"The group '{name}' does not exist.")
        else:
            return group

    def to_representation(self, value: Group) -> str:
        return f"Group: {value.name}"


class PhotoHashField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Photo:
        return get_object_or_404(Photo, md5=data)

    def to_representation(self, value: Photo) -> str:
        return value.md5


class TagField(serializers.RelatedField):
    def to_internal_value(self, data: str) -> Tag:
        slug = slugify(data)

        if not slug:
            raise ValidationError("Tag name can't be empty.")

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
            raise ValidationError(f"The user '{name}' does not exist.")
        else:
            return user

    def to_representation(self, value: User) -> str:
        return value.username.capitalize()
