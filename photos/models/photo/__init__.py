from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_save, post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.http import HttpRequest
from django.urls import reverse

from rest_framework.request import Request

from photos.fields import JSONField
from photos.models.photo.utils import (
    check_dimensions, parse_exif_data, parse_xmp_data,
    format_f_stop, get_exif)
from photos.settings import (
    MEDIA_FOLDERS as MEDIA, DEFAULT_PATH, COLOR_CHOICES, COLOR_WHITE)

import os
from typing import Optional, Union


def get_filename(photo: 'Photo', filename: str, ext: Optional[str] = None) -> str:
    if ext is None:
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')

    ts = photo.taken.strftime("%Y%m%d_%H%M%S")

    return f"{ts}_{photo.short_md5}.{ext}"


def get_original_path(photo: 'Photo', filename: str) -> str:
    return f"{MEDIA['ORIGINAL']}/{get_filename(photo, filename)}"


def get_display_path(photo: 'Photo', filename: str) -> str:
    return f"{MEDIA['DISPLAY']}/{get_filename(photo, filename)}"


def get_thumbnail_path(photo: 'Photo', filename: str) -> str:
    return f"{MEDIA['THUMBNAIL']}/{get_filename(photo, filename, ext='jpg')}"


def get_square_thumbnail_path(photo: 'Photo', filename: str) -> str:
    return f"{MEDIA['SQUARE']}/{get_filename(photo, filename, ext='jpg')}"


class Photo(models.Model):
    # Original image

    original = models.ImageField(
        upload_to=get_original_path,
        verbose_name="Original image",
        help_text="Original image with no modifications")
    md5 = models.CharField(
        max_length=32, editable=False, unique=True, verbose_name="MD5")

    sidecar_exists = models.BooleanField(default=False)
    original_filename = models.CharField(max_length=1000, blank=True)

    # Display image

    watermark = models.CharField(
        max_length=1, choices=COLOR_CHOICES, default=COLOR_WHITE, blank=True)
    image = models.ImageField(
        upload_to=get_display_path,
        blank=True, null=True, editable=False,
        verbose_name="Display image",
        help_text="Smaller image with watermark applied")

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    file_size = models.CharField(
        max_length=50, editable=False, blank=True)

    # Thumbnails

    thumbnail = models.ImageField(
        upload_to=get_thumbnail_path, blank=True, null=True, editable=False)
    square_thumbnail = models.ImageField(
        upload_to=get_square_thumbnail_path, blank=True, null=True, editable=False)

    # Metadata

    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, related_name='photos',
        blank=True, null=True)

    taken = models.DateTimeField(editable=False)
    edited = models.DateTimeField(editable=False)
    uploaded = models.DateTimeField(auto_now_add=True, editable=False)

    exif = JSONField(blank=True, verbose_name="EXIF")

    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.filename

    @property
    def access_level(self):
        if self.album is None:
            from photos.models.album import Allow
            return Allow.PUBLIC

        return self.album.access_level

    def check_access(self, request: Union[HttpRequest, Request]) -> bool:
        if self.album is None:
            return True

        return self.album.check_access(request)

    def clean(self) -> None:
        if self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5")

        super().clean()

    def delete(self, using=None, keep_parents=False) -> None:
        self.original.delete(save=False)
        self.image.delete(save=False)
        self.thumbnail.delete(save=False)
        self.square_thumbnail.delete(save=False)

        super().delete(using=using, keep_parents=keep_parents)

    @property
    def filename(self) -> str:
        return os.path.basename(self.original.name)

    def generate_image(self, image_type: str, save: bool = False) -> None:
        file = self.get_original()

        if image_type == 'display_image':
            from photos.tasks import update_display_image
            function = update_display_image
        elif image_type == 'thumbnail':
            from photos.tasks import update_thumbnail
            function = update_thumbnail
        elif image_type == 'square_thumbnail':
            from photos.tasks import update_square_thumbnail
            function = update_square_thumbnail
        else:
            return

        function(self, file)

        if save:
            self.save()

    def get_absolute_url(self) -> str:
        return reverse('photo', args=[self.album.path, self.md5])

    def get_access_code_url(self) -> str:
        return self.get_absolute_url() + self.album.get_access_code_query()

    def get_download_url(self) -> str:
        return reverse('download', kwargs={'path': self.path, 'md5': self.md5})

    def get_exif(self) -> dict:
        return get_exif(self)

    def get_image_file(self, image_type: str) -> Optional[ImageFieldFile]:
        if image_type == 'original':
            return self.original
        elif image_type == 'display_image':
            return self.image
        elif image_type == 'square_thumbnail':
            return self.square_thumbnail
        elif image_type == 'thumbnail':
            return self.thumbnail
        else:
            raise ValueError

    def get_image_filename(self, image_type: str) -> Optional[str]:
        file = self.get_image_file(image_type)
        return file.name if file is not None else None

    def get_image_filename_candidate(self, image_type: str) -> Optional[str]:
        if image_type == 'original':
            function = get_original_path
        elif image_type == 'display_image':
            function = get_display_path
        elif image_type == 'square_thumbnail':
            function = get_square_thumbnail_path
        elif image_type == 'thumbnail':
            function = get_thumbnail_path
        else:
            raise ValueError

        filename = self.get_image_filename(image_type)
        return function(self, filename) if filename is not None else None

    def get_original(self) -> File:
        file = cache.get(self.md5)

        if file is None:
            file = self.original.file

        return file

    @property
    def path(self) -> str:
        return self.album.path if self.album else DEFAULT_PATH

    def resave(self) -> None:
        if not self.pk:
            return

        delete = []

        for field_name in 'original', 'image', 'thumbnail', 'square_thumbnail':
            image: ImageFieldFile = getattr(self, field_name)

            # Mark the old file for deletion
            delete.append(image.name)

            # Resave the files: the new path is automatically determined
            filename = os.path.basename(image.name)
            image.save(filename, File(image), save=False)

        try:
            # Save the new paths
            self.save()
        except:
            pass
        else:
            # Delete the old files
            storage = DefaultStorage()

            for name in delete:
                storage.delete(name)

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            super().save(*args, **kwargs)
            return

        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: photos_photo.md5":
                self.delete()
                raise ValidationError(f"Duplicate file: {self.md5}")

    @property
    def short_md5(self) -> str:
        return self.md5[:8]

    class Meta:
        get_latest_by = 'taken'
        ordering = ('taken', 'uploaded')


@receiver(pre_save, sender=Photo,
          dispatch_uid='photos.models.process_image_upload')
def process_image_upload(sender, instance: Photo, **kwargs) -> None:
    photo = instance

    if photo.pk is not None:
        return

    file = photo.get_original()
    file.seek(0)

    check_dimensions(file)
    parse_exif_data(photo, file)
    parse_xmp_data(photo, file)

    file.seek(0)
    photo.original.save(file.name, File(file), save=False)


@receiver(post_save, sender=Photo,
          dispatch_uid='photos.models.create_sidecar_images')
def create_sidecar_images(sender, instance: Photo, created: bool, **kwargs) -> None:
    if not created:
        return

    photo = instance

    from photos.tasks import create_sidecar_images
    create_sidecar_images.delay(photo.pk)
