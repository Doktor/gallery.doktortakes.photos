from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from photos.fields import JSONField
from photos.settings import PANORAMAS_FOLDER, PANORAMA_THUMBNAILS_FOLDER
from photos.models.utils import (
    DATE_FORMAT, format_file_size, generate_md5_hash, get_modified_time_utc)

import datetime
import exifread
import os
import PIL.Image
import pytz
import uuid
from io import BytesIO

strptime = datetime.datetime.strptime


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
