from django.core.files import File

from photos.models import Photo
from photos.models.album import SIZE_3600
from photos.models.utils import format_file_size
from photos.models.photo.utils import (
    apply_watermark, fit_image, fit_image_long_edge, guess_aspect_ratio)
from photos.settings_photos import (
    SQUARE_THUMBNAIL_SIZE, THUMBNAIL_QUALITY,  WATERMARKS_ENABLED)


import datetime
import PIL.Image
from celery import shared_task
from io import BytesIO
from typing import Tuple

strptime = datetime.datetime.strptime


@shared_task
def create_sidecar_images(pk: int) -> None:
    photo = Photo.objects.get(pk=pk)
    file = photo.get_original()

    update_display_image(photo, file)
    update_square_thumbnail(photo, file)

    if photo.rating >= 4:
        update_thumbnail(photo, file)

    photo.file_size = format_file_size(photo.image.size)
    photo.sidecar_exists = True
    photo.save()

    if hasattr(file, 'close'):
        file.close()


# Update


def update_display_image(photo: Photo, file: File) -> None:
    edge = 3600 if photo.album.thumbnail_size == SIZE_3600 else 2400
    image, (w, h) = create_display_image(file, edge, photo.watermark)

    if photo.image:
        photo.image.delete(save=False)

    photo.width = w
    photo.height = h
    photo.image.save(photo.filename, File(image), save=False)


def update_square_thumbnail(photo: Photo, file: File) -> None:
    image = PIL.Image.open(file)
    generated = fit_image(image, SQUARE_THUMBNAIL_SIZE)

    new_file = BytesIO()
    generated.save(new_file, 'JPEG', quality=THUMBNAIL_QUALITY, optimize=True)

    if photo.square_thumbnail:
        photo.square_thumbnail.delete(save=False)

    photo.square_thumbnail.save(photo.filename, File(new_file), save=False)


def update_thumbnail(photo: Photo, file: File) -> None:
    image = PIL.Image.open(file)
    generated = fit_image_long_edge(image, 1200)

    new_file = BytesIO()
    generated.save(new_file, 'JPEG', quality=THUMBNAIL_QUALITY, optimize=True)

    if photo.thumbnail:
        photo.thumbnail.delete(save=False)

    photo.thumbnail.save(photo.filename, File(new_file), save=False)


# Helper functions


def create_display_image(data: File, long_edge: int, watermark_color: str) -> (BytesIO, Tuple[int, int]):
    image = PIL.Image.open(data)
    w, h = image.size

    # Save EXIF metadata for later
    try:
        exif = image.info['exif']
    except KeyError:
        exif = None

    # Resize the image
    ratio = guess_aspect_ratio(w, h)

    if w > h:
        long, short = long_edge, int(long_edge / ratio)
        size = long, short
    else:
        long, short = long_edge, int(long_edge / (1 / ratio))
        size = short, long

    image = fit_image(image, size)

    # Add watermark
    if WATERMARKS_ENABLED:
        image = apply_watermark(image, watermark_color)

    # Save image data and re-add EXIF metadata
    data = BytesIO()

    if exif is not None:
        image.save(data, 'JPEG', quality=90, exif=exif)
    else:
        image.save(data, 'JPEG', quality=90)

    return data, image.size
