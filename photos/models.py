from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from django.conf import settings

from photos.fields import JSONField
from photos.settings import (
    MEDIA_FOLDERS, DEFAULT_PATH,
    PANORAMAS_FOLDER, PANORAMA_THUMBNAILS_FOLDER,
    WATERMARKS_ENABLED, WATERMARK_IMAGES, WATERMARK_OFFSET,
    COLOR_CHOICES, COLOR_NONE, COLOR_WHITE, COLOR_BLACK)

import datetime
import exifread
import hashlib
import os
import PIL.Image
import pytz
import uuid
from io import BytesIO
from lxml import etree

fromtimestamp = datetime.datetime.fromtimestamp
strptime = datetime.datetime.strptime

CHUNK_SIZE = 64 * 1024  # 64 KB

DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


# Helper functions


def format_file_size(b):
    """Returns a human-readable string representation of a number of bytes."""
    for unit in ('B', 'KB', 'MB', 'GB'):
        if abs(b) < 1024.0:
            return "%3.2f %s" % (b, unit)
        b /= 1024.0
    return "%.2f %s" % (b, 'TB')


def get_modified_time_utc(file):
    storage = DefaultStorage()
    return storage.get_modified_time(file.name)


# Album

SIZE_2400 = '2400'
SIZE_3600 = '3600'

SIZES = (
    (SIZE_2400, '2400 x 1600'),
    (SIZE_3600, '3600 x 2400'),
)


class Album(models.Model):
    """A collection of photos and albums."""

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


albums_to_move = {}


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


# Tag


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Tag: #{self.slug}"


# Photo


def get_path(photo, filename, ext=None):
    if ext is None:
        base, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')
    else:
        base, _ = os.path.splitext(filename)

    return f"{photo.get_path()}/{base}.{ext}"


def get_original_path(photo, filename):
    return f"{MEDIA_FOLDERS['ORIGINAL']}/{get_path(photo, filename)}"


def get_display_path(photo, filename):
    return f"{MEDIA_FOLDERS['DISPLAY']}/{get_path(photo, filename)}"


def get_thumbnail_path(photo, filename):
    return f"{MEDIA_FOLDERS['THUMBNAIL']}/" \
           f"{get_path(photo, filename, ext='jpg')}"


def get_square_thumbnail_path(photo, filename):
    return f"{MEDIA_FOLDERS['SQUARE']}/" \
           f"{get_path(photo, filename, ext='jpg')}"


def generate_md5_hash(file):
    hasher = hashlib.md5()

    for chunk in file.chunks(chunk_size=CHUNK_SIZE):
        hasher.update(chunk)

    return hasher.hexdigest()


XMP_START = b'<x:xmpmeta'
XMP_END = b'</x:xmpmeta>'

NS = {
    'x': "adobe:ns:meta/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'xmp': "http://ns.adobe.com/xap/1.0/"
}


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


# Panoramas

def get_panorama_path(pano, filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.')

    if pano.pk is not None:
        return f"{pano.md5}.{ext}"
    else:
        return f"{uuid.uuid4()}.{ext}"


def get_panorama_image_path(pano, filename):
    return f"{PANORAMAS_FOLDER}/{get_panorama_path(pano, filename)}"


def get_panorama_thumbnail_path(pano, filename):
    return f"{PANORAMA_THUMBNAILS_FOLDER}/{get_panorama_path(pano, filename)}"


class Panorama(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    location = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to=get_panorama_image_path,
        width_field='width', height_field='height')
    md5 = models.CharField(
        max_length=32, editable=False, unique=True, verbose_name="MD5")

    thumbnail = models.ImageField(
        upload_to=get_panorama_thumbnail_path, editable=False, null=True)

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    file_size = models.CharField(max_length=50, editable=False)

    timezone = models.CharField(max_length=100, default='US/Eastern')
    taken = models.DateTimeField(editable=False, null=True)
    edited = models.DateTimeField(editable=False, null=True)
    uploaded = models.DateTimeField(auto_now=True, editable=False)

    exif = JSONField(editable=False, null=True, blank=True, verbose_name="EXIF")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('panorama', kwargs={'slug': self.slug})

    def get_thumbnail_size(self):
        return format_file_size(self.thumbnail.size)


@receiver(pre_save, sender=Panorama,
          dispatch_uid='photos.models.update_panorama')
def update_panorama(sender, instance, **kwargs):
    pano = instance

    if hasattr(pano, '_rename'):
        return

    # Update fields if a new instance was created, or the image was changed
    try:
        previous = Panorama.objects.get(pk=pano.pk)
    except Panorama.DoesNotExist:
        pass
    else:
        if previous.image != pano.image:
            # Delete the old image file
            previous.image.delete(save=False)
        else:
            return

    pano._update = True

    pano.image.open()

    # Save the new image file under a temporary name
    # The post-save handler renames the file to match the new MD5 hash
    pano.image.save(pano.image.name, pano.image, save=False)

    # Generate a thumbnail
    tb = create_panorama_thumbnail(pano)

    if pano.thumbnail:
        pano.thumbnail.delete(save=False)

    pano.thumbnail.save(pano.image.name, File(tb), save=False)

    pano.image.open()

    # File size
    pano.file_size = format_file_size(pano.image.size)

    # MD5 hash
    md5 = generate_md5_hash(pano.image)

    try:
        Panorama.objects.get(md5=md5)
    except Panorama.DoesNotExist:
        pano.md5 = md5
    else:
        raise ValidationError(f"Duplicate file detected: {md5}")

    # EXIF data
    exif = exifread.process_file(pano.image, details=False)

    pano.exif = {k: v.printable for k, v in exif.items()}

    # Timestamps
    modified = get_modified_time_utc(pano.image)

    tz_name = pano.timezone
    tz = pytz.timezone(tz_name)

    taken = pano.exif.get('EXIF DateTimeDigitized', None)
    if taken is not None:
        pano.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
    else:
        pano.taken = modified

    edited = pano.exif.get('Image DateTime', None)
    if edited is not None:
        pano.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
    else:
        pano.edited = modified

    pano.image.close()


@receiver(post_save, sender=Panorama,
          dispatch_uid='photos.models.rename_panorama_files')
def rename_panorama_files(sender, instance, created, **kwargs):
    pano = instance

    if hasattr(pano, '_update'):
        del pano._update

        fields = ['image', 'thumbnail']

        for field in fields:
            file = getattr(pano, field)
            path_method = globals()[f"get_panorama_{field}_path"]

            old_path = file.path
            new_name = path_method(pano, file.name)
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            file.name = new_name
            os.rename(old_path, new_path)

        # Done!
        pano._rename = True
        pano.save()


def create_panorama_thumbnail(pano):
    pano.image.open()

    image = PIL.Image.open(pano.image)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    image.thumbnail((3000, 3000))

    data = BytesIO()
    image.save(data, 'JPEG', quality=80, optimize=True)

    pano.image.close()

    return data
