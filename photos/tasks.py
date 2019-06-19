from django.core.files import File

from photos.settings import (
    WATERMARKS_ENABLED, WATERMARK_IMAGES, WATERMARK_OFFSET)
from photos.models import Photo
from photos.models.album import SIZE_3600
from photos.models.utils import format_file_size
from photos.utils import thumbnail

import datetime
import PIL.Image
from celery import shared_task
from io import BytesIO
from typing import Union

strptime = datetime.datetime.strptime


def replace_square_thumbnail(photo: Photo, image: File) -> None:
    sq = create_square_thumbnail(image)

    if photo.square_thumbnail:
        photo.square_thumbnail.delete(save=False)

    photo.square_thumbnail.save(photo.filename, File(sq), save=False)


def replace_display_image(photo: Photo, image: File) -> None:
    edge = 3600 if photo.album.thumbnail_size == SIZE_3600 else 2400

    im, w, h = create_display_image(image, edge, photo.watermark)

    if photo.image:
        photo.image.delete(save=False)

    photo.width = w
    photo.height = h
    photo.image.save(photo.filename, File(im), save=False)


def replace_thumbnail(photo: Photo, image: File) -> None:
    tb = create_thumbnail(image)

    if photo.thumbnail:
        photo.thumbnail.delete(save=False)

    photo.thumbnail.save(photo.filename, File(tb), save=False)


@shared_task
def create_sidecar_images(pk: int) -> None:
    photo: Photo = Photo.objects.get(pk=pk)
    file = photo.get_original()

    replace_square_thumbnail(photo, file)
    replace_display_image(photo, file)

    if photo.rating >= 4:
        replace_thumbnail(photo, file)

    photo.file_size = format_file_size(photo.image.size)

    photo.sidecar_exists = True
    photo.save()

    if hasattr(file, 'close'):
        file.close()


def create_thumbnail(data: Union[File, BytesIO], size=(1200, 800)) -> BytesIO:
    long, short = size

    image = PIL.Image.open(data)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    w, h = image.size

    if w > h:
        size = (long, short)
    elif w < h:
        size = (short, long)
    else:
        size = (long, long)

    image = thumbnail(image, size)

    data = BytesIO()
    image.save(data, 'JPEG', quality=80, optimize=True)

    return data


def create_square_thumbnail(data: Union[File, BytesIO], size=(400, 400)) -> BytesIO:
    image = PIL.Image.open(data)

    if image.format != 'JPEG':
        image = image.convert('RGB')

    image = thumbnail(image, size)

    data = BytesIO()
    image.save(data, 'JPEG', quality=75, optimize=True)

    return data


TOLERANCE = 1 / 1000
RESAMPLE = PIL.Image.LANCZOS
RATIOS = (3 / 2, 16 / 9, 2.35 / 1)


def create_display_image(data: Union[File, BytesIO], edge: int, wm) -> (BytesIO, int, int):
    image = PIL.Image.open(data)

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
        watermark = WATERMARK_IMAGES.get((edge, wm), None)

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

    return data, width, height
