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

from core.context_processors import metadata
from photos.models.utils import Status
from photos.settings import MEDIA_FOLDERS

import os
from typing import Tuple, Optional, List

m = metadata(None)

SIZE_2400 = '2400'
SIZE_3600 = '3600'

SIZES = (
    (SIZE_2400, '2400 x 1600'),
    (SIZE_3600, '3600 x 2400'),
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

    hidden = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)

    users = models.ManyToManyField(User, related_name='albums', blank=True)
    groups = models.ManyToManyField(Group, related_name='albums', blank=True)

    tags = models.ManyToManyField('Tag', related_name='albums', blank=True)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        if self.end is not None and self.end < self.start:
            raise ValidationError(
                "The end date should be later than the start date.")

    @property
    def count(self) -> int:
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

    WRONG_PASSWORD = Status(1, "Incorrect password specified.")
    NO_PASSWORD = Status(2, "This album doesn't have a password but one was specified.")

    def check_access(self, request: HttpRequest) -> Tuple[bool, Optional[Status]]:
        user = request.user
        password = request.GET.get('password', None)

        access = False
        status = None

        # If a password is given but the album doesn't have a password
        if password is not None and not self.password:
            status = self.NO_PASSWORD

        # Staff users have access to everything
        if user.is_staff:
            access = True

            if password is not None and self.password and password != self.password:
                status = self.WRONG_PASSWORD

            return access, status

        # Access list does not exist
        if not self.users.exists() and not self.groups.exists():
            access = True
        # Access list exists and it's an anonymous user
        elif not user.is_authenticated:
            access = False

        if user in self.users.all():
            access = True
        elif any(group in user.groups.all() for group in self.groups.all()):
            access = True
        elif self.password:
            access = password == self.password

        return access, status

    def delete(self, using=None, keep_parents=False) -> None:
        for photo in self.photos.all():
            photo.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self) -> str:
        return reverse('album', args=[self.get_path()])

    def get_access_list(self) -> str:
        names = []

        for user in self.users.all():
            names.append(user.username.capitalize())
        for group in self.groups.all():
            names.append(f"Group: {group.name}")

        return ', '.join(names)

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
        return reverse('edit_album', args=[self.get_path()])

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
                previous=self.slug + divider + previous, divider=divider)

    def get_place(self) -> str:
        if self.place or not self.parent:
            return self.place

        return self.parent.get_place()

    def get_parent_path(self) -> str:
        return self.parent.get_path() if self.parent is not None else ''

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

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        self.clean()
        super().save(*args, **kwargs)

    def serialize(self, edit: bool = False) -> dict:
        if self.end:
            end = self.end.strftime("%Y-%m-%d")
        else:
            end = None

        response = {
            'url': self.get_absolute_url(),
            'name': self.name,
            'slug': self.slug,
            'path': self.get_path(),
            'place': self.place,
            'location': self.location,
            'description': self.description,
            'start': self.start.strftime("%Y-%m-%d"),
            'end': end,
            'hidden': str(self.hidden).lower(),
            'password': self.password,
            'access': self.get_access_list(),
            'tags': ', '.join((tag.slug for tag in self.tags.all())),
            'parent': self.get_parent_path(),
        }

        if self.cover is not None:
            response['cover'] = {
                'url': self.cover.image.url,
                'thumbnail_url': self.cover.thumbnail.url,
            }

        if edit:
            response.update({
                'edit_url': self.get_edit_url(),
                'title': f"Editing {self.name} | {m.get('TITLE')}"
            })

        return response

    class Meta:
        get_latest_by = 'start'
        unique_together = ('name', 'parent')


@receiver(m2m_changed, sender=Album.users.through,
          dispatch_uid="photos.models.check_hidden.users")
@receiver(m2m_changed, sender=Album.groups.through,
          dispatch_uid="photos.models.check_hidden.groups")
def check_hidden(sender, instance: Album, action: str, **kwargs) -> None:
    album = instance

    if not action.startswith('post'):
        return

    hidden = album.users.exists() or album.groups.exists() or album.password != ''

    # Prevent extra saves
    if album.hidden == hidden:
        return

    album.hidden = hidden
    album.save()


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

    from photos.tasks import update_thumbnail
    update_thumbnail(album.cover, album.cover.get_original())
    album.cover.save()


@receiver(post_delete, sender=Album,
          dispatch_uid="photos.models.delete_album_folders")
def delete_album_folders(sender, instance: Album, **kwargs) -> None:
    album = instance

    storage = DefaultStorage()
    path = album.get_path()

    for name in MEDIA_FOLDERS.values():
        folder_path = os.path.join(name, path)

        if storage.exists(folder_path):
            storage.delete(folder_path)
