from django.core.files import File

from photos.models import Photo
from photos.models.photo.photo import COLOR_WHITE
from photos.models.photo.thumbnail import (
    THUMBNAIL_COVER, THUMBNAIL_DISPLAY, THUMBNAIL_LARGE_SQUARE,
    THUMBNAIL_SMALL_SQUARE)
from photos.models.photo.watermark import WATERMARK_COLOR_BLACK, WATERMARK_COLOR_WHITE
from photos.settings_photos import LARGE_SQUARE_THUMBNAIL_WIDTH, SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_QUALITY
from photos.utils.image import create_thumbnail, guess_aspect_ratio

import datetime
import PIL.Image
from typing import Tuple

strptime = datetime.datetime.strptime


def create_thumbnails(photo: Photo, file: File) -> None:
    update_display_image(photo, file)
    update_square_thumbnail(photo, file)

    if photo.rating >= 4:
        update_thumbnail(photo, file)

    photo.sidecar_exists = True
    photo.save()

    if hasattr(file, 'close'):
        file.close()


# Update


def update_display_image(photo: Photo, file: File) -> None:
    long_edge = int(photo.album.display_image_size)
    width, height = get_thumbnail_size_preserve_ratio(file, long_edge)

    if False and photo.watermark is not None:
        watermark_color = WATERMARK_COLOR_WHITE if photo.watermark == COLOR_WHITE else WATERMARK_COLOR_BLACK

        create_thumbnail(
            photo, file,
            width, height, THUMBNAIL_DISPLAY,
            quality=90, add_watermark=True, watermark_color=watermark_color)
    else:
        create_thumbnail(
            photo, file,
            width, height, THUMBNAIL_DISPLAY,
            quality=90)


def update_square_thumbnail(photo: Photo, file: File) -> None:
    create_thumbnail(
        photo, file,
        SQUARE_THUMBNAIL_WIDTH, SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_SMALL_SQUARE,
        quality=THUMBNAIL_QUALITY)


def update_large_square_thumbnail(photo: Photo, file: File) -> None:
    create_thumbnail(
        photo, file,
        LARGE_SQUARE_THUMBNAIL_WIDTH, LARGE_SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_LARGE_SQUARE,
        quality=THUMBNAIL_QUALITY)


def update_thumbnail(photo: Photo, file: File) -> None:
    long_edge = 1200
    width, height = get_thumbnail_size_preserve_ratio(file, long_edge)

    create_thumbnail(
        photo, file,
        width, height, THUMBNAIL_COVER,
        quality=THUMBNAIL_QUALITY)


# Helper functions


def get_thumbnail_size_preserve_ratio(data: File, long_edge: int) -> Tuple[int, int]:
    image = PIL.Image.open(data)
    w, h = image.size

    # Resize the image
    ratio = guess_aspect_ratio(w, h)

    if w > h:
        return long_edge, int(long_edge / ratio)
    else:
        return int(long_edge / (1 / ratio)), long_edge
