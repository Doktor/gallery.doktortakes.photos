from django.core.files import File

from photos.models import Photo
from photos.models.photo.thumbnail import (
    THUMBNAIL_LARGE_SQUARE,
    THUMBNAIL_MEDIUM_SQUARE,
    THUMBNAIL_SMALL_SQUARE,
    THUMBNAIL_EXTRA_SMALL_SQUARE,
    THUMBNAIL_MEDIUM)
from photos.settings_photos import (
    EXTRA_SMALL_SQUARE_THUMBNAIL_WIDTH,
    MEDIUM_SQUARE_THUMBNAIL_WIDTH,
    LARGE_SQUARE_THUMBNAIL_WIDTH,
    SQUARE_THUMBNAIL_WIDTH,
    MEDIUM_THUMBNAIL_SIZE,
    THUMBNAIL_QUALITY)
from photos.utils.image import create_thumbnail

import datetime
import PIL.Image
from typing import Tuple

strptime = datetime.datetime.strptime


def create_thumbnails(photo: Photo, file: File) -> None:
    update_extra_small_square_thumbnail(photo, file)
    update_medium_square_thumbnail(photo, file)
    update_medium_thumbnail(photo, file)

    photo.sidecar_exists = True
    photo.save()

    if hasattr(file, 'close'):
        file.close()


# Update


def update_display_image(photo: Photo, file: File) -> None:
    return


def update_extra_small_square_thumbnail(photo: Photo, file: File) -> None:
    create_thumbnail(
        photo, file,
        EXTRA_SMALL_SQUARE_THUMBNAIL_WIDTH, EXTRA_SMALL_SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_EXTRA_SMALL_SQUARE,
        quality=THUMBNAIL_QUALITY)


def update_square_thumbnail(photo: Photo, file: File) -> None:
    return


def update_medium_square_thumbnail(photo: Photo, file: File) -> None:
    create_thumbnail(
        photo, file,
        MEDIUM_SQUARE_THUMBNAIL_WIDTH, MEDIUM_SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_MEDIUM_SQUARE,
        quality=THUMBNAIL_QUALITY)


def update_large_square_thumbnail(photo: Photo, file: File) -> None:
    create_thumbnail(
        photo, file,
        LARGE_SQUARE_THUMBNAIL_WIDTH, LARGE_SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_LARGE_SQUARE,
        quality=THUMBNAIL_QUALITY)


def update_medium_thumbnail(photo: Photo, file: File) -> None:
    width, height = get_thumbnail_size_preserve_ratio(file, MEDIUM_THUMBNAIL_SIZE)

    create_thumbnail(
        photo, file,
        width, height, THUMBNAIL_MEDIUM,
        quality=THUMBNAIL_QUALITY)


def update_thumbnail(photo: Photo, file: File) -> None:
    return


# Helpers


def get_thumbnail_size_preserve_ratio(data: File, long_size: int) -> Tuple[int, int]:
    image = PIL.Image.open(data)

    w, h = image.size
    ratio = max(w, h) / min(w, h)

    long = long_size
    short = int(long_size / ratio)

    if w > h:
        return (long, short)
    else:
        return (short, long)
