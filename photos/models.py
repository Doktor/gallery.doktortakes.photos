from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from photos import settings
from photos.fields import JSONField

import datetime
import exifread
import hashlib
import os
import PIL.Image
import pytz
import uuid
from io import BytesIO

fromtimestamp = datetime.datetime.fromtimestamp
strptime = datetime.datetime.strptime

BLOCK_SIZE = 1 * 1024 * 1024  # 1 MB

CROP = (
    ('C', 'Center'),
    ('U', 'Up'),
    ('R', 'Right'),
    ('D', 'Down'),
    ('L', 'Left'),
)

DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


def format_file_size(b):
    """Returns a human-readable string representation of a number of bytes."""
    for unit in ('B', 'KB', 'MB', 'GB'):
        if abs(b) < 1024.0:
            return "%3.2f %s" % (b, unit)
        b /= 1024.0
    return "%.2f %s" % (b, 'TB')


def get_modified_time_utc(filename):
    """Returns the modification time (UTC) of a file."""
    ts = os.path.getmtime(filename)
    return fromtimestamp(ts, pytz.UTC)


def get_cover_folder(album, original_name):
    """Returns the upload path for an album cover thumbnail."""
    _, ext = os.path.splitext(original_name)
    return ".cover/{name}.{ext}".format(
        name=album.get_path(divider='_'), ext=ext.lstrip('.'))


class Album(models.Model):
    """A collection of photos and albums."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    location = models.CharField(
        max_length=128, blank=True,
        help_text="Where the photos in this album were taken")
    timezone = models.CharField(max_length=100, default='US/Eastern')
    description = models.CharField(
        max_length=1000, blank=True,
        help_text="A brief description of this album")

    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    cover = models.OneToOneField(
        'Photo', models.SET_NULL,
        related_name='cover_for', blank=True, null=True,
        help_text="The cover photo for this album")
    thumbnail = models.ImageField(
        upload_to=get_cover_folder, blank=True, null=True)
    crop = models.CharField(
        max_length=1, default='C', choices=CROP,
        help_text="The side of the photo to crop the cover thumbnail to")

    parent = models.ForeignKey(
        'self', models.SET_NULL,
        related_name='children', blank=True, null=True,
        help_text="The album that contains this album")

    @property
    def count(self):
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

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

    def get_delete_url(self):
        """Returns the URL for deleting this album."""
        return reverse('delete_album', args=[self.get_path()])

    def __str__(self):
        return self.name

    def clean(self):
        if self.end is not None and self.end < self.start:
            raise ValidationError("End date should be after start date")
        super(Album, self).clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = 'start'
        unique_together = ('name', 'parent')


@receiver(pre_save, sender=Album, dispatch_uid="models.album.name")
def update_name(sender, instance, *args, **kwargs):
    album = instance

    # Prevents infinite loop
    if hasattr(album, '_rename'):
        return

    try:
        previous = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if previous.name == album.name:
            return

    old_path = previous.get_path()
    new_path = album.get_path()

    # Rename the media folder
    old_media = os.path.join(settings.MEDIA_ROOT, old_path)
    new_media = os.path.join(settings.MEDIA_ROOT, new_path)

    try:
        os.rename(old_media, new_media)
    except FileNotFoundError as e:
        raise e

    # Rename the thumbnails folder
    old_thumb = os.path.join(
        settings.MEDIA_ROOT, settings.THUMBNAIL_DIR, old_path)
    new_thumb = os.path.join(
        settings.MEDIA_ROOT, settings.THUMBNAIL_DIR, new_path)

    try:
        os.rename(old_thumb, new_thumb)
    except FileNotFoundError as e:
        raise e

    # Update the paths of all the photos in the album
    for photo in Photo.objects.filter(album=album):
        photo.image.name = os.path.join(
            new_path, os.path.basename(photo.image.name))
        photo.thumbnail.name = os.path.join(
            settings.THUMBNAIL_DIR, new_path,
            os.path.basename(photo.thumbnail.name))

        try:
            photo._rename = True
            photo.save()
        finally:
            del photo._rename

    if album.thumbnail:
        try:
            album._rename = True

            album.thumbnail.open()
            thumb = ContentFile(album.thumbnail.read())
            album.thumbnail.close()

            album.thumbnail.save(album.cover.filename, thumb, save=False)
        finally:
            del album._rename


# noinspection PyUnusedLocal
@receiver(pre_save, sender=Album, dispatch_uid="models.album.cover")
def update_cover(sender, instance, *args, **kwargs):
    """Updates the cover thumbnail for an album."""
    album = instance

    # Album thumbnail shouldn't be regenerated when renaming files
    if hasattr(album, '_rename'):
        return

    try:
        previous = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        if not album.cover:
            return
        else:
            thumb = create_album_thumbnail(album)
    else:
        if ((album.cover and not album.thumbnail) or
                (previous.cover != album.cover) or
                (previous.crop != album.crop)):
            thumb = create_album_thumbnail(album)
        else:
            return

    # Delete the existing thumbnail, if it exists
    if album.thumbnail:
        album.thumbnail.delete(save=False)

    album.thumbnail.save(album.cover.filename, File(thumb), save=False)


@receiver(pre_delete, sender=Album, dispatch_uid="models.album.delete")
def delete_album(sender, instance, *args, **kwargs):
    """Deletes related files when an album is deleted."""
    album = instance

    if album.thumbnail:
        album.thumbnail.delete(save=False)

    for photo in album.photos.all():
        photo.thumbnail.delete(save=False)
        photo.image.delete(save=False)


def create_album_thumbnail(album, size=(800, 600)):
    """Creates a cover for the given album."""
    album.cover.image.open()

    image = PIL.Image.open(album.cover.image)
    crop = album.crop

    if image.format != 'JPEG':
        image = image.convert('RGB')

    # Upscale small images
    if image.size < size:
        w, h = image.size
        ratio = max(size[0] / w, size[1] / h)
        image = image.resize((w * ratio, h * ratio), PIL.Image.BICUBIC)

    w, h = image.size

    mid_w = w * 1 / 2
    mid_h = h * 1 / 2

    new_w = h * 4 / 3
    new_h = w * 3 / 4

    if w > h:
        if w >= new_w:
            y1 = 0
            y2 = h
            if crop in ['C', 'U', 'D']:
                x1 = mid_w - new_w * 1 / 2
                x2 = mid_w + new_w * 1 / 2
            elif crop == 'L':
                x1 = 0
                x2 = new_w
            elif crop == 'R':
                x1 = w - new_w
                x2 = w
        else:
            x1 = 0
            x2 = w
            if crop in ['C', 'L', 'R']:
                y1 = mid_h - new_h * 1 / 2
                y2 = mid_h + new_h * 1 / 2
            elif crop == 'U':
                y1 = 0
                y2 = new_h
            elif crop == 'D':
                y1 = h - new_h
                y2 = h
    elif w < h:
        if h >= new_h:
            x1 = 0
            x2 = w
            if crop in ['C', 'L', 'R']:
                y1 = mid_h - new_h * 1 / 2
                y2 = mid_h + new_h * 1 / 2
            elif crop == 'U':
                y1 = 0
                y2 = new_h
            elif crop == 'D':
                y1 = h - new_h
                y2 = h
        else:
            y1 = 0
            y2 = h
            if crop in ['C', 'U', 'D']:
                x1 = mid_w - new_w * 1 / 2
                x2 = mid_w + new_w * 1 / 2
            elif crop == 'L':
                x1 = 0
                x2 = new_w
            elif crop == 'R':
                x1 = w - new_w
                x2 = w
    elif w == h:
        x1 = 0
        x2 = w
        y1 = mid_h - new_h * 1 / 2
        y2 = mid_h + new_h * 1 / 2

    bounds = map(int, (x1, y1, x2, y2))
    image = image.crop(bounds)
    image.thumbnail(size, PIL.Image.ANTIALIAS)

    # Fixes rounding errors
    bounds = (0, 0, size[0], size[1])
    image = image.crop(bounds)

    data = BytesIO()
    image.save(data, "JPEG", quality=75, optimize=True)

    album.cover.image.close()

    return data


def get_photo_path(photo, filename, ext=None):
    if ext is None:
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.')

    if photo.pk is not None:
        return f"{photo.album.get_path()}/{photo.md5}.{ext}"
    else:
        return f"{photo.album.get_path()}/{uuid.uuid4()}.{ext}"


def get_photo_image_path(photo, filename):
    return f"photos/{get_photo_path(photo, filename)}"


def get_photo_thumbnail_path(photo, filename):
    return f"thumbs/{get_photo_path(photo, filename, ext='jpg')}"


def generate_md5_hash(filename):
    h = hashlib.md5()

    with open(filename, 'rb') as f:
        buf = f.read(BLOCK_SIZE)

        while len(buf) > 0:
            h.update(buf)
            buf = f.read(BLOCK_SIZE)

    return h.hexdigest()


class Photo(models.Model):
    image = models.ImageField(
        upload_to=get_photo_image_path,
        width_field='width', height_field='height')
    md5 = models.CharField(max_length=32, editable=False, unique=True)

    thumbnail = models.ImageField(
        upload_to=get_photo_thumbnail_path, editable=False,
        help_text="Automatically generated thumbnail")
    crop = models.CharField(
        max_length=1, default='C', choices=CROP,
        help_text="The side of the photo to crop the thumbnail to")

    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, related_name='photos')

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    file_size = models.CharField(max_length=50, editable=False)

    taken = models.DateTimeField(
        editable=False,
        help_text="When this photo was taken")
    edited = models.DateTimeField(
        editable=False,
        help_text="When this photo was edited")

    exif = JSONField(editable=False, blank=True)

    @property
    def dimensions(self):
        """Returns the dimensions of the photo as a string in the format
        {width}x{height}."""
        return "{0}x{1}".format(self.width, self.height)

    @property
    def filename(self):
        """Returns the filename of the photo file."""
        return os.path.basename(self.image.name)

    def get_absolute_url(self):
        """Returns the URL for this photo."""
        return reverse('photo', args=[self.album.get_path(), self.md5])

    def __str__(self):
        return f"Photo {self.md5}"

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
            return

        self.image.open()

        # File size
        self.file_size = format_file_size(self.image.size)

        # MD5 hash
        self.md5 = generate_md5_hash(self.image.name)

        try:
            Photo.objects.get(md5=self.md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise ValidationError(f"Duplicate file detected: {self.md5}")

        # EXIF data
        exif = exifread.process_file(self.image)
        exif.pop('JPEGThumbnail', None)  # Discard the embedded thumbnail

        self.exif = {k: v.printable for k, v in exif.items()}

        # Timestamps
        modified = get_modified_time_utc(self.image.name)

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
            self.taken = modified

        self.image.close()

        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'taken'
        ordering = ['taken']
        unique_together = ('album', 'taken')


@receiver(post_save, sender=Photo,
          dispatch_uid='photos.models.rename_photo_files')
def rename_photo_files(sender, instance, created, *args, **kwargs):
    """Renames image files after a photo is created or updated."""
    photo = instance

    # Existing object, new image
    if hasattr(photo, '_update'):
        assert not created
        del photo._update

        # We only have to rename the image: the old thumbnail is deleted in
        # the pre-save receiver, which frees up the filename for the new file
        image = photo.image
        current_path = image.path
        image.name = get_photo_image_path(photo, image.name)

        os.remove(image.path)
        os.rename(current_path, image.path)

        photo._rename = True
        photo.save()
        return

    if not created:
        return

    # Rename the image file
    image = photo.image
    old_path = image.path
    image.name = get_photo_image_path(photo, image.name)
    os.rename(old_path, image.path)

    # Rename the thumbnail file
    thumbnail = photo.thumbnail
    old_path = thumbnail.path
    thumbnail.name = get_photo_thumbnail_path(photo, thumbnail.name)
    os.rename(old_path, thumbnail.path)

    photo._rename = True
    photo.save()


# noinspection PyUnusedLocal
@receiver(pre_save, sender=Photo)
def update_thumbnail(sender, instance, *args, **kwargs):
    """Updates the thumbnail for a photo."""
    photo = instance

    # Thumbnails shouldn't be regenerated when renaming files
    if hasattr(photo, '_rename'):
        return

    try:
        previous = Photo.objects.get(pk=photo.pk)
    # New photo
    except Photo.DoesNotExist:
        tb = create_photo_thumbnail(photo)
    else:
        # Updated file
        if previous.image != photo.image:
            tb = create_photo_thumbnail(photo)
        else:
            return

    # Delete the existing thumbnail, if it exists
    if photo.thumbnail:
        photo.thumbnail.delete(save=False)

    photo.thumbnail.save(photo.filename, File(tb), save=False)


def create_photo_thumbnail(photo, size=(400, 400)):
    """Creates a thumbnail of the given photo."""
    photo.image.open()

    image = PIL.Image.open(photo.image)
    crop = photo.crop

    if image.format != 'JPEG':
        image = image.convert('RGB')

    # Upscale small images
    if image.size < size:
        w, h = image.size
        ratio = max(size[0] / w, size[1] / h)
        image = image.resize((w * ratio, h * ratio), PIL.Image.BICUBIC)

    w, h = image.size

    if w > h:
        y1 = 0
        y2 = h
        if crop in ['C', 'U', 'D']:
            x1 = 0.5 * w - 0.5 * h
            x2 = 0.5 * w + 0.5 * h
        elif crop == 'L':
            x1 = 0
            x2 = h
        elif crop == 'R':
            x1 = w - h
            x2 = w
    elif w < h:
        x1 = 0
        x2 = w
        if crop in ['C', 'L', 'R']:
            y1 = 0.5 * h - 0.5 * w
            y2 = 0.5 * h + 0.5 * w
        elif crop == 'U':
            y1 = 0
            y2 = w
        elif crop == 'D':
            y1 = h - w
            y2 = h
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

    photo.image.close()

    return data
