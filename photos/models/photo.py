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

from core import settings
from photos.fields import JSONField
from photos.models.utils import DATE_FORMAT, get_modified_time_utc
from photos.settings import (
    MEDIA_FOLDERS as MEDIA, DEFAULT_PATH, ITEMS_IN_FILMSTRIP,
    COLOR_CHOICES, COLOR_NONE, COLOR_WHITE, COLOR_BLACK,
    CHECK_MINIMUM_SIZE, MINIMUM_LONG_EDGE, MINIMUM_SHORT_EDGE)

import datetime
import exifread
import os
import PIL.Image
import pytz
from lxml import etree
from typing import Optional, Union

strptime = datetime.datetime.strptime

XMP_START = b'<x:xmpmeta'
XMP_END = b'</x:xmpmeta>'

NS = {
    'x': "adobe:ns:meta/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'xmp': "http://ns.adobe.com/xap/1.0/"
}

IMAGE_TYPES = ['original', 'display_image', 'square_thumbnail', 'thumbnail']


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

    local_path = models.CharField(max_length=1000, blank=True)

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
            if self.local_path and os.path.isfile(self.local_path):
                file = open(self.local_path, 'rb')
            else:
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


def check_dimensions(file: File) -> None:
    """Checks the dimensions of an uploaded image and raises a ValidationError
    if the image is too small."""

    if not CHECK_MINIMUM_SIZE:
        return

    image = PIL.Image.open(file)
    long, short = max(*image.size), min(*image.size)

    if long < MINIMUM_LONG_EDGE or short < MINIMUM_SHORT_EDGE:
        raise ValidationError(
            "The uploaded image is too small: the minimum size is "
            f"{MINIMUM_LONG_EDGE}x{MINIMUM_SHORT_EDGE} px, "
            f"but the uploaded image was {long}x{short} px.")


def parse_exif_data(photo: Photo, file: File) -> None:
    """Extracts EXIF data from an image and adds it to a Photo object."""

    file.seek(0)
    raw_exif = exifread.process_file(file, details=False, debug=False)
    photo.exif = {k: v.printable for k, v in raw_exif.items()}

    # Timestamps
    modified = get_modified_time_utc(file)
    tz = pytz.utc

    taken = photo.exif.get('EXIF DateTimeOriginal', None)
    if taken is not None:
        photo.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.taken = modified

    edited = photo.exif.get('Image DateTime', None)
    if edited is not None:
        photo.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.edited = modified


def parse_xmp_data(photo: Photo, file: File) -> None:
    """Extracts XMP data from an image and adds it to a Photo object."""

    file.seek(0)
    data = file.read()
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


def format_f_stop(f: str) -> float:
    """Takes an f-stop as a fractional string and converts it to a number."""
    try:
        f = f.split('/')
    except AttributeError:
        return 0
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return float(f[0])


def get_exif(photo: Photo) -> dict:
    e = photo.exif

    camera = e.get('Image Model', 'Camera unknown')

    try:
        make = e.get('EXIF LensMake', e['Image Make'])
        model = e['EXIF LensModel']

        lens = f'{make} {model}'
    except KeyError:
        lens = 'Lens unknown'

    if 'EF-S' in lens:
        lens = lens.replace('EF-S', 'EF-S ')
    elif 'EF' in lens:
        lens = lens.replace('EF', 'EF ')

    try:
        focal_length = f"{e['EXIF FocalLength']} mm"
    except KeyError:
        focal_length = 'Unknown'

    try:
        shutter_speed = f"{e['EXIF ExposureTime']} s"
    except KeyError:
        shutter_speed = 'Unknown'

    try:
        f_stop = f"f/{format_f_stop(e['EXIF FNumber'])}"
    except KeyError:
        if camera != 'Camera unknown':
            f_stop = 'f/0'
        else:
            f_stop = 'Unknown'

    try:
        iso_speed = f"ISO {e['EXIF ISOSpeedRatings']}"
    except KeyError:
        iso_speed = 'Unknown'

    return {
        'camera': camera,
        'lens': lens,
        'focal_length': focal_length,
        'shutter_speed': shutter_speed,
        'aperture': f_stop,
        'iso_speed': iso_speed,
    }
