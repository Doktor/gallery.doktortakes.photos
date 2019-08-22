from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.signals import pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.http import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from rest_framework.request import Request

from core.context_processors import metadata
from photos.settings import MEDIA_FOLDERS

import os
from typing import List, Union

m = metadata(None)

SIZE_2400 = '2400'
SIZE_3600 = '3600'

SIZES = (
    (SIZE_2400, '2400 x 1600'),
    (SIZE_3600, '3600 x 2400'),
)


class Allow:
    PUBLIC = 0
    SIGNED_IN = 10
    OWNERS = 20
    STAFF = 30
    SUPERUSER = 100


ACCESS_LEVELS = (
    (Allow.PUBLIC, "Public"),
    (Allow.SIGNED_IN, "Signed in"),
    (Allow.OWNERS, "Owners"),
    (Allow.STAFF, "Staff"),
    (Allow.SUPERUSER, "Superusers"),
)


class Album(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)

    place = models.CharField(
        max_length=128, blank=True,
        help_text="The specific venue, building, or place")
    location = models.CharField(
        max_length=128, blank=True,
        help_text="The city, state, and country")
    timezone = models.CharField(max_length=100, default='US/Eastern')
    description = models.CharField(
        max_length=1000, blank=True,
        help_text="A brief description of this album")

    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)

    thumbnail_size = models.CharField(
        max_length=4, choices=SIZES, default=SIZE_2400)

    cover = models.OneToOneField(
        'Photo', models.SET_NULL,
        related_name='cover_for', blank=True, null=True,
        help_text="The cover photo for this album")

    parent = models.ForeignKey(
        'self', models.SET_NULL,
        related_name='children', blank=True, null=True,
        help_text="The album that contains this album")

    path = models.TextField(
        blank=True, editable=False,
        help_text="The path to this album; automatically set")

    # Permissions
    access_level = models.PositiveSmallIntegerField(
        choices=ACCESS_LEVELS, default=Allow.PUBLIC)

    password = models.CharField(max_length=128, blank=True)
    users = models.ManyToManyField(User, related_name='albums', blank=True)
    groups = models.ManyToManyField(Group, related_name='albums', blank=True)

    tags = models.ManyToManyField('Tag', related_name='albums', blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def allow_public(self) -> bool:
        return self.access_level == Allow.PUBLIC

    def clean(self) -> None:
        if self.parent == self:
            raise ValidationError("An album can't be its own parent.")

        if self.end is not None and self.end < self.start:
            raise ValidationError(
                "The end date should be later than the start date.")

    @property
    def count(self) -> int:
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

    def check_access(self, request: Union[HttpRequest, Request]) -> bool:
        album = self
        user = request.user

        if user.is_superuser:
            return True

        try:
            password = request.GET['password']
        except KeyError:
            password = False

        # Password access supersedes all other permission checks
        if album.password and password and album.password == password:
            return True

        elif album.access_level == Allow.PUBLIC:
            return True

        elif album.access_level == Allow.SIGNED_IN:
            return user.is_authenticated

        elif album.access_level == Allow.OWNERS:
            if user in album.users.all():
                return True
            elif any(group in user.groups.all() for group in album.groups.all()):
                return True
            else:
                return False

        elif album.access_level == Allow.STAFF:
            return user.is_staff

        elif album.access_level == Allow.SUPERUSER:
            return user.is_superuser

    def delete(self, using=None, keep_parents=False) -> None:
        for photo in self.photos.all():
            photo.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self) -> str:
        return reverse('album', args=[self.path])

    def get_all_subalbums(self, include_self: bool = False) -> List['Album']:
        albums = []

        if include_self:
            albums.append(self)

        for album in self.children.all():
            albums += album.get_all_subalbums(include_self=True)

        return albums

    def get_all_subphotos(self, include_self: bool = False) -> List['Photo']:
        photos = []

        if include_self:
            photos += list(self.photos.all())

        for album in self.children.all():
            photos += album.get_all_subphotos(include_self=True)

        return photos

    def get_edit_url(self) -> str:
        return reverse('edit_album', args=[self.path])

    def get_full_date(self) -> str:
        template = "{date:%a} {date.year}-{date.month:02}-{date.day:02}"

        if not self.end or self.start == self.end:
            full_date = template.format(date=self.start)
        else:
            full_date = "{start} &ndash; {end}".format(
                start=template.format(date=self.start),
                end=template.format(date=self.end))

        return mark_safe(full_date)

    def get_full_location(self) -> str:
        place = self.get_place()
        location = self.get_location()

        if place and location:
            return f"{place}, {location}"
        elif place:
            return place
        elif location:
            return location
        else:
            return ''

    def get_groups(self) -> str:
        return ', '.join(f'Group: {group.name}' for group in self.groups.all())

    def get_location(self) -> str:
        if self.location or not self.parent:
            return self.location

        return self.parent.get_location()

    def get_path(self, previous='', divider='/') -> str:
        if not self.parent:
            if not previous:
                return self.slug
            else:
                return self.slug + divider + previous

        if not previous:
            return self.parent.get_path(
                previous=self.slug, divider=divider)
        else:
            return self.parent.get_path(
                previous=f"{self.slug}{divider}{previous}", divider=divider)

    def get_place(self) -> str:
        if self.place or not self.parent:
            return self.place

        return self.parent.get_place()

    def get_password_query(self, separator: bool = False) -> str:
        if self.password:
            q = f"?password={self.password}"

            if separator:
                return q + '&'
            return q
        else:
            return ''

    def get_password_url(self) -> str:
        return self.get_absolute_url() + self.get_password_query()

    def get_users(self) -> str:
        return ', '.join(user.username.capitalize() for user in self.users.all())

    def save(self, *args, **kwargs) -> None:
        self.clean()

        self.slug = slugify(self.name)
        self.path = self.get_path()

        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'start'
        unique_together = ('name', 'parent')


@receiver(pre_save, sender=Album,
          dispatch_uid="photos.models.create_album_cover")
def create_album_cover(sender, instance: Album, **kwargs) -> None:
    album = instance

    try:
        prev = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if prev.cover == album.cover:
            return

        if album.cover is None:
            return

    from photos.tasks import update_thumbnail
    update_thumbnail(album.cover, album.cover.get_original())
    album.cover.save()


@receiver(post_delete, sender=Album,
          dispatch_uid="photos.models.delete_album_folders")
def delete_album_folders(sender, instance: Album, **kwargs) -> None:
    album = instance
    storage = DefaultStorage()

    for name in MEDIA_FOLDERS.values():
        folder_path = os.path.join(name, album.path)

        if storage.exists(folder_path):
            storage.delete(folder_path)
