from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from photos.settings import MEDIA_FOLDERS

import os


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
    password = models.CharField(max_length=128, blank=True, null=True)

    tags = models.ManyToManyField('Tag', related_name='albums', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.end is not None and self.end < self.start:
            raise ValidationError(
                "The end date should be later than the start date.")
        super().clean()

    @property
    def count(self):
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

    def delete(self, using=None, keep_parents=False):
        for photo in self.photos.all():
            photo.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def get_all_subalbums(self, include_self=False):
        albums = []

        if include_self:
            albums.append(self)

        for album in self.children.all():
            albums += album.get_all_subalbums(include_self=True)

        return albums

    def get_all_subphotos(self, include_self=False):
        photos = []

        if include_self:
            photos += list(self.photos.all())

        for album in self.children.all():
            photos += album.get_all_subphotos(include_self=True)

        return photos

    def get_full_date(self):
        formatter = "{date:%A}, {date:%B} {date.day}, {date.year}"
        if not self.end or self.start == self.end:
            date = formatter.format(date=self.start)
        else:
            date = "{start} &mdash; {end}".format(
                start=formatter.format(date=self.start),
                end=formatter.format(date=self.end))
        return mark_safe(date)

    def get_full_location(self):
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

    def get_location(self):
        if self.location or not self.parent:
            return self.location

        return self.parent.get_location()

    def get_place(self):
        if self.place or not self.parent:
            return self.place

        return self.parent.get_place()

    def get_path(self, previous='', divider='/'):
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

    def get_absolute_url(self):
        return reverse('album', args=[self.get_path()])

    def get_edit_url(self):
        return reverse('edit_album', args=[self.get_path()])

    def get_hidden_url(self):
        return self.get_absolute_url() + self.get_password_query()

    def get_password_query(self):
        return f"?password={self.password}&" if self.password else ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'start'
        unique_together = ('name', 'parent')


@receiver(pre_save, sender=Album,
          dispatch_uid="photos.models.create_album_cover")
def create_album_cover(sender, instance, **kwargs):
    album: Album = instance

    try:
        prev = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if prev.cover == album.cover:
            return

    from photos.tasks import replace_thumbnail
    replace_thumbnail(album.cover)


albums_to_move = {}


@receiver(pre_save, sender=Album,
          dispatch_uid="photos.models.check_album_path")
def check_album_path(sender, instance, **kwargs):
    album: Album = instance

    if not album.get_all_subphotos(include_self=True):
        return

    try:
        prev = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if prev.get_path() == album.get_path():
            return

    albums_to_move[album] = prev.get_path()


@receiver(post_save, sender=Album,
          dispatch_uid="photos.models.move_album_files")
def move_album_files(sender, instance, created, **kwargs):
    album: Album = instance

    if album not in albums_to_move.keys():
        return

    for photo in album.get_all_subphotos(include_self=True):
        photo.resave()

    storage = DefaultStorage()
    path = albums_to_move.pop(album)

    for folder in MEDIA_FOLDERS.values():
        storage.delete(os.path.join(folder, path))


@receiver(post_delete, sender=Album,
          dispatch_uid="photos.models.delete_album_folders")
def delete_album_folders(sender, instance, **kwargs):
    album: Album = instance

    storage = DefaultStorage()
    path = album.get_path()

    for name in MEDIA_FOLDERS.values():
        folder_path = os.path.join(name, path)

        if storage.exists(folder_path):
            storage.delete(folder_path)
