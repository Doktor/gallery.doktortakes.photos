from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from django.conf import settings

from photos.settings import (
    MEDIA_FOLDERS, DEFAULT_PATH,
    PANORAMAS_FOLDER, PANORAMA_THUMBNAILS_FOLDER,
    LANDSCAPE_SIZE, PORTRAIT_SIZE,
    WATERMARKS_ENABLED, WATERMARK_IMAGES, WATERMARK_OFFSET,
    WATERMARK_COLOR_CHOICES,
    WATERMARK_COLOR_NONE, WATERMARK_COLOR_WHITE, WATERMARK_COLOR_BLACK)

from photos.fields import JSONField

import datetime
import exifread
import hashlib
import os
import PIL.Image
import pytz
import uuid
import warnings
from contextlib import contextmanager
from io import BytesIO
from libxmp import XMPFiles as XMP, consts as XMPConstants

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
    """Returns the modification time (UTC) of a file."""
    storage = DefaultStorage()
    return storage.get_modified_time(file.name)


# Album


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

    tags = models.ManyToManyField('Tag', related_name='albums')

    @property
    def count(self):
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

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
            photos += list(Photo.objects.filter(album=self))

        for album in self.children.all():
            photos += album.get_all_subphotos(include_self=True)

        return photos

    def get_full_date(self):
        """Returns this album's date, including its end date if specified,
        as a string."""
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
        """Returns the path to this album."""
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
        """Returns the URL for this album."""
        return reverse('album', args=[self.get_path()])

    def get_edit_url(self):
        """Returns the URL for editing this album."""
        return reverse('edit_album', args=[self.get_path()])

    def get_hidden_url(self):
        return self.get_absolute_url() + self.get_password_query()

    def get_password_query(self):
        return f"?password={self.password}" if self.password else ''

    def __str__(self):
        return self.name

    def clean(self):
        if self.end is not None and self.end < self.start:
            raise ValidationError(
                "The end date should be later than the start date.")
        super().clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'start'
        unique_together = ('name', 'parent')


@receiver(pre_save, sender=Album,
          dispatch_uid="photos.models.update_album_name")
def update_album_name(sender, instance, *args, **kwargs):
    album = instance

    if album.photos.count() == 0:
        return

    # Prevents an infinite loop
    if hasattr(album, '_rename'):
        return

    try:
        old = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if old.get_path() == album.get_path():
            return

    fallback = False

    old_path = old.get_path()
    new_path = album.get_path()

    # Move the media folders
    folders = MEDIA_FOLDERS.values()

    for folder in folders:
        base = os.path.join(settings.MEDIA_ROOT, folder)

        old_dir = os.path.join(base, old_path)
        new_dir = os.path.join(base, new_path)

        try:
            os.rename(old_dir, new_dir)
        except FileNotFoundError:
            fallback = True
            warnings.warn(
                f"Media folder '{old_dir}' not found, trying fallback method")

    if fallback:
        # Fallback method if the folders are named incorrectly
        # This should be fixed now, but just in case...

        # Find the path by checking the path of any photo in the album
        photo = album.photos.all()[0]
        path, _ = os.path.split(photo.original.name)
        old_path = path.replace(MEDIA_FOLDERS['ORIGINAL'] + '/', '')

        for folder in folders:
            base = os.path.join(settings.MEDIA_ROOT, folder)

            old_dir = os.path.join(base, old_path)
            new_dir = os.path.join(base, new_path)

            try:
                os.rename(old_dir, new_dir)
            except FileNotFoundError as e:
                raise e

    # Update photo file paths
    for photo in Photo.objects.filter(album=album):
        photo.original.name = os.path.join(
            MEDIA_FOLDERS['ORIGINAL'],
            new_path,
            os.path.basename(photo.original.name))

        photo.image.name = os.path.join(
            MEDIA_FOLDERS['DISPLAY'],
            new_path,
            os.path.basename(photo.image.name))

        photo.thumbnail.name = os.path.join(
            MEDIA_FOLDERS['THUMBNAIL'],
            new_path,
            os.path.basename(photo.thumbnail.name))

        photo.square_thumbnail.name = os.path.join(
            MEDIA_FOLDERS['SQUARE'],
            new_path,
            os.path.basename(photo.square_thumbnail.name))

        try:
            photo._rename = True
            photo.save()
        finally:
            del photo._rename


@receiver(pre_delete, sender=Album, dispatch_uid="photos.models.delete_album")
def delete_album(sender, instance, *args, **kwargs):
    """Deletes related files when an album is deleted."""
    album = instance

    for photo in album.photos.all():
        photo.image.delete(save=False)
        photo.thumbnail.delete(save=False)


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


def get_photo_path(photo, filename, ext=None):
    if ext is None:
        base, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')
    else:
        base, _ = os.path.splitext(filename)

    return f"{photo.get_path()}/{base}.{ext}"


def get_photo_image_path(photo, filename):
    return f"{MEDIA_FOLDERS['ORIGINAL']}/{get_photo_path(photo, filename)}"


def get_photo_display_path(photo, filename):
    return f"{MEDIA_FOLDERS['DISPLAY']}/{get_photo_path(photo, filename)}"


def get_photo_thumbnail_path(photo, filename):
    return f"{MEDIA_FOLDERS['THUMBNAIL']}/" \
           f"{get_photo_path(photo, filename, ext='jpg')}"


def get_photo_square_thumbnail_path(photo, filename):
    return f"{MEDIA_FOLDERS['SQUARE']}/" \
           f"{get_photo_path(photo, filename, ext='jpg')}"


def generate_md5_hash(file):
    hasher = hashlib.md5()

    for chunk in file.chunks(chunk_size=CHUNK_SIZE):
        hasher.update(chunk)

    return hasher.hexdigest()


class Photo(models.Model):
    # Original image

    original = models.ImageField(
        upload_to=get_photo_image_path,
        verbose_name="Original image",
        help_text="Original image with no modifications")
    md5 = models.CharField(
        max_length=32, editable=False, unique=True, verbose_name="MD5")

    # Display image

    watermark = models.CharField(
        max_length=1, choices=WATERMARK_COLOR_CHOICES,
        default=WATERMARK_COLOR_WHITE, blank=True)
    image = models.ImageField(
        upload_to=get_photo_display_path, editable=False,
        width_field='width', height_field='height',
        verbose_name="Display image",
        help_text="Smaller image with watermark applied")

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    file_size = models.CharField(
        max_length=50, editable=False, blank=True)

    # Thumbnails

    thumbnail = models.ImageField(
        upload_to=get_photo_thumbnail_path, editable=False)
    square_thumbnail = models.ImageField(
        upload_to=get_photo_square_thumbnail_path, editable=False)

    # Metadata

    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, related_name='photos',
        blank=True, null=True)

    taken = models.DateTimeField(editable=False)
    edited = models.DateTimeField(editable=False)
    uploaded = models.DateTimeField(auto_now_add=True, editable=False)

    exif = JSONField(blank=True, verbose_name="EXIF")

    rating = models.PositiveSmallIntegerField(default=0)

    @property
    def filename(self):
        """Returns the filename of the photo file."""
        return os.path.basename(self.original.name)

    @property
    def original_width(self):
        return self.original.width

    @property
    def original_height(self):
        return self.original.height

    def get_absolute_url(self):
        """Returns the URL for this photo."""
        return reverse('photo', args=[self.album.get_path(), self.md5])

    def get_path(self):
        return self.album.get_path() if self.album else DEFAULT_PATH

    def __str__(self):
        return self.filename

    def clean(self):
        if self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5")

        super().clean()

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
            return

        self.original.open()

        self.original.save(self.original.name, self.original, save=False)

        # MD5 hash
        self.md5 = generate_md5_hash(self.original)

        try:
            Photo.objects.get(md5=self.md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise ValidationError(f"Duplicate file detected: {self.md5}")

        # EXIF data
        exif = exifread.process_file(self.original, details=False)

        self.exif = {k: v.printable for k, v in exif.items()}

        # XMP data
        # python-xmp-toolkit doesn't accept file objects, so we need a local
        # copy of the file
        try:
            local = True

            # If using local storage, this is simple
            path = self.original.path
        except NotImplementedError:
            local = False

            # If using remote storage, save a temporary copy to the local disk
            _, ext = os.path.splitext(self.original.name)
            filename = os.path.join('temp', f"{uuid.uuid4()}{ext}")

            os.makedirs(os.path.join(settings.BASE_DIR, 'temp'), exist_ok=True)

            with open(os.path.join(settings.BASE_DIR, filename), 'wb') as f:
                for chunk in self.original.chunks(chunk_size=CHUNK_SIZE):
                    f.write(chunk)

            path = os.path.abspath(filename)

        # Process the file
        xmp = XMP(file_path=path).get_xmp()

        try:
            rating = xmp.get_property(XMPConstants.XMP_NS_XMP, 'Rating')
            self.rating = int(rating)
        except (AttributeError, ValueError):
            self.rating = 0

        try:
            label = xmp.get_property(XMPConstants.XMP_NS_XMP, 'Label').lower()
        except AttributeError:
            self.watermark = WATERMARK_COLOR_NONE
        else:
            self.watermark = (WATERMARK_COLOR_BLACK if label == 'green' else
                              WATERMARK_COLOR_WHITE)

        # If using remote storage, remove the temporary copy
        if not local:
            os.remove(path)

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

        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'taken'
        ordering = ('taken', 'uploaded')


@contextmanager
def temp_file():
    os.makedirs(os.path.join(settings.BASE_DIR, 'temp'), exist_ok=True)
    filename = os.path.join('temp', str(uuid.uuid4()) + '.jpg')
    path = os.path.abspath(filename)

    yield path

    os.remove(path)


@receiver(post_save, sender=Photo,
          dispatch_uid='photos.models.update_display_image')
def update_display_image(sender, instance, created, *args, **kwargs):
    if not created:
        return

    photo = instance

    if hasattr(photo, '_display'):
        del photo._display
        return

    with temp_file() as path:
        # Make a copy of the file
        with open(path, 'wb') as f:
            photo.original.open()

            for chunk in photo.original.chunks(chunk_size=CHUNK_SIZE):
                f.write(chunk)

            photo.original.close()

        # Resize and apply watermark
        with open(path, 'rb') as f:
            xmp_f = XMP(file_path=path)
            xmp = xmp_f.get_xmp()

            # Load the image
            image = PIL.Image.open(f)
            exif = image.info['exif']

            # Resize the image
            width, height = image.size

            if width > height:
                resize = LANDSCAPE_SIZE
            else:
                resize = PORTRAIT_SIZE

            image = image.resize(resize, resample=PIL.Image.LANCZOS)
            width, height = image.size

            if WATERMARKS_ENABLED:
                watermark = WATERMARK_IMAGES.get(photo.watermark)
                offset = WATERMARK_OFFSET

                x = width - watermark.size[0] - offset
                y = height - watermark.size[1] - offset
                coords = (x, y)

                image.paste(watermark, coords, mask=watermark.split()[3])

            image.save(path, 'JPEG', quality=95, exif=exif)

            # Re-add XMP data
            xmp_f = XMP(file_path=path, open_forupdate=True)
            xmp_f.put_xmp(xmp)
            xmp_f.close_file()

        # Save it to the model
        with open(path, 'rb') as f:
            photo._display = True
            photo.image.save(photo.filename, File(f), save=True)

        # Update metadata
        photo.image.open()

        # File size
        photo.file_size = format_file_size(photo.image.size)

        photo.image.close()
        photo._display = True
        photo.save()


@receiver(pre_save, sender=Photo,
          dispatch_uid='photos.models.update_photo_thumbnails')
def update_photo_thumbnails(sender, instance, *args, **kwargs):
    """Updates the thumbnails for a photo."""
    photo = instance

    # Don't regenerate thumbnails when renaming files
    if hasattr(photo, '_rename'):
        return

    try:
        _ = Photo.objects.get(pk=photo.pk)
    except Photo.DoesNotExist:
        tb = create_photo_thumbnail(photo)
        sq = create_photo_square_thumbnail(photo)
    else:
        if hasattr(photo, '_resave'):
            tb = create_photo_thumbnail(photo)
            sq = create_photo_square_thumbnail(photo)
            del photo._resave
        else:
            return

    if photo.thumbnail:
        photo.thumbnail.delete(save=False)

    if photo.square_thumbnail:
        photo.square_thumbnail.delete(save=False)

    photo.thumbnail.save(photo.filename, File(tb), save=False)
    photo.square_thumbnail.save(photo.filename, File(sq), save=False)


def create_photo_thumbnail(photo):
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

    # Upscale small images
    if image.size < size:
        w, h = image.size
        ratio = max(size[0] / w, size[1] / h)
        new_w, new_h = int(w * ratio), int(h * ratio)

        image = image.resize((new_w, new_h), PIL.Image.BICUBIC)

    image.thumbnail(size)

    data = BytesIO()
    image.save(data, 'JPEG', quality=80, optimize=True)

    photo.original.close()

    return data


def create_photo_square_thumbnail(photo, size=(400, 400)):
    """Creates a square thumbnail of the given photo."""
    photo.original.open()

    image = PIL.Image.open(photo.original)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    # Upscale small images
    if image.size < size:
        w, h = image.size
        ratio = max(size[0] / w, size[1] / h)
        new_w, new_h = int(w * ratio), int(h * ratio)

        image = image.resize((new_w, new_h), PIL.Image.BICUBIC)

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

    def get_thumbnail_size(self):
        return format_file_size(self.thumbnail.size)

    def get_absolute_url(self):
        return reverse('panorama', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Panorama,
          dispatch_uid='photos.models.update_panorama')
def update_panorama(sender, instance, *args, **kwargs):
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
def rename_panorama_files(sender, instance, created, *args, **kwargs):
    """Renames image files after a panorama is created or updated."""
    pano = instance

    if hasattr(pano, '_update'):
        del pano._update

        fields = ['image', 'thumbnail']

        for field in fields:
            file = getattr(pano, field)
            get_path = globals()[f"get_panorama_{field}_path"]

            old_path = file.path
            new_name = get_path(pano, file.name)
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            file.name = new_name
            os.rename(old_path, new_path)

        # Done!
        pano._rename = True
        pano.save()


def create_panorama_thumbnail(pano):
    """Creates a thumbnail of the given photo."""
    pano.image.open()

    image = PIL.Image.open(pano.image)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    image.thumbnail((3000, 3000))

    data = BytesIO()
    image.save(data, 'JPEG', quality=80, optimize=True)

    pano.image.close()

    return data
