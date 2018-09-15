from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_save, post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.urls import reverse

from photos.fields import JSONField
from photos.settings import (
    MEDIA_FOLDERS as MEDIA, DEFAULT_PATH,
    COLOR_CHOICES, COLOR_NONE, COLOR_WHITE, COLOR_BLACK)
from photos.models.utils import (
    CHUNK_SIZE, DATE_FORMAT, get_modified_time_utc)

import datetime
import exifread
import os
import pytz
from io import BytesIO
from lxml import etree

strptime = datetime.datetime.strptime

XMP_START = b'<x:xmpmeta'
XMP_END = b'</x:xmpmeta>'

NS = {
    'x': "adobe:ns:meta/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'xmp': "http://ns.adobe.com/xap/1.0/"
}


def get_path(photo, filename, ext=None):
    if ext is None:
        base, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')
    else:
        base, _ = os.path.splitext(filename)

    return f"{photo.get_path()}/{base}.{ext}"


def get_original_path(photo, filename):
    return f"{MEDIA['ORIGINAL']}/{get_path(photo, filename)}"


def get_display_path(photo, filename):
    return f"{MEDIA['DISPLAY']}/{get_path(photo, filename)}"


def get_thumbnail_path(photo, filename):
    return f"{MEDIA['THUMBNAIL']}/{get_path(photo, filename, ext='jpg')}"


def get_square_thumbnail_path(photo, filename):
    return f"{MEDIA['SQUARE']}/{get_path(photo, filename, ext='jpg')}"


class Photo(models.Model):
    # Original image

    original = models.ImageField(
        upload_to=get_original_path,
        verbose_name="Original image",
        help_text="Original image with no modifications")
    md5 = models.CharField(
        max_length=32, editable=False, unique=True, verbose_name="MD5")

    sidecar_exists = models.BooleanField(default=False)

    # Display image

    watermark = models.CharField(
        max_length=1, choices=COLOR_CHOICES, default=COLOR_WHITE, blank=True)
    image = models.ImageField(
        upload_to=get_display_path, editable=False,
        width_field='width', height_field='height',
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

    def __str__(self):
        return self.filename

    def clean(self):
        if self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5")

        super().clean()

    def delete(self, using=None, keep_parents=False):
        self.original.delete(save=False)
        self.image.delete(save=False)
        self.thumbnail.delete(save=False)
        self.square_thumbnail.delete(save=False)

        super().delete(using=using, keep_parents=keep_parents)

    @property
    def filename(self):
        return os.path.basename(self.original.name)

    def get_absolute_url(self):
        return reverse('photo', args=[self.album.get_path(), self.md5])

    def get_path(self):
        return self.album.get_path() if self.album else DEFAULT_PATH

    def resave(self):
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

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
            return

        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: photos_photo.md5":
                self.delete()

                from photos.api.utils import APIError
                raise APIError(f"Duplicate file: {self.md5}")

    class Meta:
        get_latest_by = 'taken'
        ordering = ('taken', 'uploaded')


@receiver(pre_save, sender=Photo,
          dispatch_uid='photos.models.parse_image_metadata')
def parse_image_metadata(sender, instance, **kwargs):
    photo = instance

    try:
        Photo.objects.get(pk=photo.pk)
    except Photo.DoesNotExist:
        pass
    else:
        return

    photo.original.open()

    # EXIF data
    exif = exifread.process_file(photo.original, details=False, debug=False)
    photo.exif = {k: v.printable for k, v in exif.items()}

    # XMP data
    raw_data = BytesIO()

    for chunk in photo.original.chunks(chunk_size=CHUNK_SIZE):
        raw_data.write(chunk)

    with raw_data as f:
        data = f.read()

        start = data.find(XMP_START)
        end = data.find(XMP_END)

        if start == -1 or end == -1:
            pass
        else:
            xml = data[start:end + len(XMP_END)].decode('utf-8')
            root = etree.fromstring(xml)

            element = root.xpath('.//rdf:Description', namespaces=NS)[0]

            try:
                rating = element.xpath('@xmp:Rating', namespaces=NS)[0]
                photo.rating = int(rating)
            except IndexError:
                photo.rating = 0

            try:
                label = element.xpath('@xmp:Label', namespaces=NS)[0].lower()
            except IndexError:
                photo.watermark = COLOR_NONE
            else:
                photo.watermark = \
                    (COLOR_BLACK if label == 'green' else COLOR_WHITE)

    # Timestamps
    modified = get_modified_time_utc(photo.original)

    if photo.album is not None:
        tz_name = photo.album.timezone
    else:
        tz_name = 'US/Eastern'

    tz = pytz.timezone(tz_name)

    taken = photo.exif.get('EXIF DateTimeDigitized', None)
    if taken is not None:
        photo.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.taken = modified

    edited = photo.exif.get('Image DateTime', None)
    if edited is not None:
        photo.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.edited = modified

    photo.original.close()


@receiver(post_save, sender=Photo,
          dispatch_uid='photos.models.create_sidecar_images')
def create_sidecar_images(sender, instance, created, **kwargs):
    photo = instance

    if not created:
        return

    from photos.tasks import create_sidecar_images
    create_sidecar_images.delay(photo.pk)
