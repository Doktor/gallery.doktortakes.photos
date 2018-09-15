from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.urls import reverse

from photos.fields import JSONField
from photos.settings import (
    MEDIA_FOLDERS, DEFAULT_PATH,
    WATERMARKS_ENABLED, WATERMARK_IMAGES, WATERMARK_OFFSET,
    MEDIA_FOLDERS as MEDIA, DEFAULT_PATH,
    COLOR_CHOICES, COLOR_NONE, COLOR_WHITE, COLOR_BLACK)
from photos.models.album import SIZE_3600
from photos.models.utils import (
    CHUNK_SIZE, DATE_FORMAT, format_file_size, get_modified_time_utc)

import datetime
import exifread
import os
import PIL.Image
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
        upload_to=get_thumbnail_path, editable=False)
    square_thumbnail = models.ImageField(
        upload_to=get_square_thumbnail_path, editable=False)

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

        self.original.open()

        # EXIF data
        exif = exifread.process_file(self.original, details=False, debug=False)
        self.exif = {k: v.printable for k, v in exif.items()}

        # XMP data
        raw_data = BytesIO()

        for chunk in self.original.chunks(chunk_size=CHUNK_SIZE):
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
                    self.rating = int(rating)
                except IndexError:
                    self.rating = 0

                try:
                    label = element.xpath('@xmp:Label', namespaces=NS)[0].lower()
                except IndexError:
                    self.watermark = COLOR_NONE
                else:
                    self.watermark = \
                        (COLOR_BLACK if label == 'green' else COLOR_WHITE)

        # Timestamps
        modified = get_modified_time_utc(self.original)

        if self.album is not None:
            tz_name = self.album.timezone
        else:
            tz_name = 'US/Eastern'

        tz = pytz.timezone(tz_name)

        taken = self.exif.get('EXIF DateTimeDigitized', None)
        if taken is not None:
            self.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
        else:
            self.taken = modified

        edited = self.exif.get('Image DateTime', None)
        if edited is not None:
            self.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
        else:
            self.edited = modified

        self.original.close()

        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: photos_photo.md5":
                self.original.delete(save=False)
                self.image.delete(save=False)
                self.thumbnail.delete(save=False)
                self.square_thumbnail.delete(save=False)

                from photos.api.utils import APIError
                raise APIError(f"Duplicate file: {self.md5}")

    class Meta:
        get_latest_by = 'taken'
        ordering = ('taken', 'uploaded')


@receiver(pre_save, sender=Photo,
          dispatch_uid='photos.models.update_sidecar_images')
def update_sidecar_images(sender, instance, **kwargs):
    photo = instance

    if hasattr(photo, '_rename'):
        return

    if hasattr(photo, '_sidecar'):
        del photo._sidecar
        return

    try:
        Photo.objects.get(pk=photo.pk)
    except Photo.DoesNotExist:
        pass
    else:
        # Shell use only
        if not hasattr(photo, '_resave'):
            return
        else:
            del photo._resave

    edge = 3600 if photo.album.thumbnail_size == SIZE_3600 else 2400

    tb = create_thumbnail(photo)
    sq = create_square_thumbnail(photo)
    im = create_display_image(photo, edge)

    if photo.thumbnail:
        photo.thumbnail.delete(save=False)

    if photo.square_thumbnail:
        photo.square_thumbnail.delete(save=False)

    if photo.image:
        photo.image.delete(save=False)

    photo.thumbnail.save(photo.filename, File(tb), save=False)
    photo.square_thumbnail.save(photo.filename, File(sq), save=False)
    photo.image.save(photo.filename, File(im), save=False)

    photo.file_size = format_file_size(photo.image.size)

    photo._sidecar = True
    photo.save()


def create_thumbnail(photo):
    """Creates a thumbnail of the given photo."""
    photo.original.open()

    long, short = (2400 / 2, 1600 / 2)

    image = PIL.Image.open(photo.original)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    w, h = image.size

    if w >= h:
        size = (long, short)
    elif w < h:
        size = (short, long)

    image.thumbnail(size)

    data = BytesIO()
    image.save(data, 'JPEG', quality=80, optimize=True)

    photo.original.close()

    return data


def create_square_thumbnail(photo, size=(400, 400)):
    """Creates a square thumbnail of the given photo."""
    photo.original.open()

    image = PIL.Image.open(photo.original)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    w, h = image.size

    if w > h:
        x1 = 0.5 * w - 0.5 * h
        y1 = 0
        x2 = 0.5 * w + 0.5 * h
        y2 = h
    elif w < h:
        x1 = 0
        y1 = 0.5 * h - 0.5 * w
        x2 = w
        y2 = 0.5 * h + 0.5 * w
    elif w == h:
        x1 = 0
        x2 = w
        y1 = 0
        y2 = h

    bounds = map(int, (x1, y1, x2, y2))
    image = image.crop(bounds)
    image.thumbnail(size)

    data = BytesIO()
    image.save(data, 'JPEG', quality=75, optimize=True)

    photo.original.close()

    return data


TOLERANCE = 1 / 1000
RESAMPLE = PIL.Image.LANCZOS
RATIOS = (3 / 2, 16 / 9, 2.35 / 1)


def create_display_image(photo, edge):
    photo.original.open()

    image = PIL.Image.open(photo.original)

    # Preserve EXIF metadata
    try:
        exif = image.info['exif']
    except KeyError:
        exif = None

    # Resize, attempting to avoid rounding errors
    width, height = image.size
    long, short = max(*image.size), min(*image.size)

    for ratio in RATIOS:
        if abs((long / short) - ratio) < TOLERANCE:
            # Resize to...
            r_long, r_short = edge, int(edge / ratio)

            if width > height:
                dims = r_long, r_short
            else:
                dims = r_short, r_long

            image = image.resize(dims, resample=RESAMPLE)
            break
    else:
        image.thumbnail((edge, edge), resample=RESAMPLE)

    width, height = image.size

    # Add watermark
    if WATERMARKS_ENABLED:
        watermark = WATERMARK_IMAGES.get((edge, photo.watermark), None)

        offset = int(WATERMARK_OFFSET * (edge / 2400))

        x = width - watermark.size[0] - offset
        y = height - watermark.size[1] - offset
        coords = (x, y)

        image.paste(watermark, coords, mask=watermark.split()[3])

    # Save and re-add EXIF metadata
    data = BytesIO()

    if exif is not None:
        image.save(data, 'JPEG', quality=90, exif=exif)
    else:
        image.save(data, 'JPEG', quality=90)

    photo.original.close()

    return data
