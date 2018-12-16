from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models import Q
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_save, post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.urls import reverse

from core import settings
from photos.fields import JSONField
from photos.settings import (
    MEDIA_FOLDERS as MEDIA, DEFAULT_PATH, ITEMS_IN_FILMSTRIP,
    COLOR_CHOICES, COLOR_NONE, COLOR_WHITE, COLOR_BLACK, LONG, SHORT)
from photos.models.utils import (
    DATE_FORMAT, get_modified_time_utc)

import datetime
import exifread
import os
import PIL.Image
import pytz
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
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')

    ts = photo.taken.strftime("%Y%m%d_%H%M%S")

    return f"{ts}_{photo.md5[:8]}.{ext}"


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

    local_path = models.CharField(max_length=1000, blank=True)

    sidecar_exists = models.BooleanField(default=False)

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

    def __str__(self):
        return self.filename

    def check_access(self, request):
        if self.album is None:
            return True

        return self.album.check_access(request)

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

    def get_original(self):
        file = cache.get(self.md5)

        if file is None:
            if self.local_path:
                file = open(self.local_path, 'rb')
            else:
                file = self.original.file

        return file

    def get_path(self):
        return self.album.get_path() if self.album else DEFAULT_PATH

    def get_password_url(self):
        return self.get_absolute_url() + self.album.get_password_query()

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

    def serialize(self, password=False, index=None, metadata=True, filmstrip=True):
        response = {
            'image_url': self.image.url,
            'square_thumbnail_url': self.square_thumbnail.url,
            'url': self.get_password_url() if password else self.get_absolute_url(),
        }

        if metadata:
            if index is None:
                index = get_index(self)

            response.update({
                'metadata': {
                    'index': index,
                    'taken': self.taken.strftime("%A, %Y-%m-%d, %-I:%M:%S %p"),
                    'width': self.width,
                    'height': self.height,
                    'md5': self.md5,
                    'new_tab': self.image.url,
                    'download': reverse(
                        'download', args=[self.get_path(), self.md5]),
                },
                'exif': get_exif(self)
            })

        if filmstrip:
            response['filmstrip'] = generate_filmstrip(self)

        return response

    class Meta:
        get_latest_by = 'taken'
        ordering = ('taken', 'uploaded')


@receiver(pre_save, sender=Photo,
          dispatch_uid='photos.models.process_image_upload')
def process_image_upload(sender, instance, **kwargs):
    photo: Photo = instance

    if photo.pk is not None:
        return

    file = photo.get_original()
    file.seek(0)

    # Check the image's dimensions and cancel the upload if it's too small
    image = PIL.Image.open(file)

    dim = image.width, image.height
    long, short = max(*dim), min(*dim)

    if not settings.TEST and (long < LONG or short < SHORT):
        raise ValidationError(
            f"Image too small: minimum {LONG}x{SHORT} px, "
            f"uploaded {long}x{short} px")

    # Load EXIF data
    file.seek(0)
    exif = exifread.process_file(file, details=False, debug=False)
    photo.exif = {k: v.printable for k, v in exif.items()}

    # Load XMP data
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

    file.seek(0)

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

    # Save the image file
    file.seek(0)
    photo.original.save(file.name, File(file), save=False)


@receiver(post_save, sender=Photo,
          dispatch_uid='photos.models.create_sidecar_images')
def create_sidecar_images(sender, instance, created, **kwargs):
    if not created:
        return

    photo = instance

    from photos.tasks import create_sidecar_images
    create_sidecar_images.delay(photo.pk)


def format_f_stop(f):
    """Takes an f-stop as a fractional string and converts it to a number."""
    try:
        f = f.split('/')
    except AttributeError:
        return 0
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return f[0]


def get_exif(p):
    e = p.exif

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
        'shutter_speed': shutter_speed,
        'aperture': f_stop,
        'iso_speed': iso_speed,
    }


def get_index(photo):
    photos = photo.album.photos.all()

    for i, item in enumerate(photos):
        if item.md5 == photo.md5:
            return i
    else:
        raise RuntimeError


def generate_filmstrip(photo):
    count = ITEMS_IN_FILMSTRIP
    half = count // 2

    album = photo.album
    all_photos = album.photos.all()

    if all_photos.count() <= count:
        photos = [*all_photos]
    else:
        # Queries
        left_q = Q(taken__lt=photo.taken) & (~Q(pk=photo.pk))
        middle_q1 = Q(taken=photo.taken, uploaded__lt=photo.uploaded)
        middle_q2 = Q(taken=photo.taken, uploaded__gt=photo.uploaded)
        right_q = Q(taken__gt=photo.taken) & (~Q(pk=photo.pk))

        # Filter...
        left = all_photos.filter(left_q).reverse()
        middle_1 = all_photos.filter(middle_q1)
        middle_2 = all_photos.filter(middle_q2)
        right = all_photos.filter(right_q)

        # Join the outside and middle queries
        left = [*left, *middle_1]
        right = [*middle_2, *right]
        lc, rc = len(left), len(right)

        if lc < half:
            deficit = count - 1 - lc
            photos = [*left, photo, *right[:deficit]]
        elif rc < half:
            deficit = count - 1 - rc
            photos = [*left[:deficit], photo, *right]
        else:
            photos = [*left[:half], photo, *right[:half]]

    photos = sorted(photos, key=lambda p: (p.taken, p.pk))

    result = []

    for photo in photos:
        result.append({
            'md5': photo.md5,
            'url': photo.square_thumbnail.url,
            'index': get_index(photo),
        })

    return result
