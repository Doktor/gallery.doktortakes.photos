from django.core.files import File

from photos.models import Photo
from photos.models.photo.thumbnail import THUMBNAIL_LARGE_SQUARE, THUMBNAIL_MEDIUM_SQUARE, THUMBNAIL_SMALL_SQUARE, THUMBNAIL_EXTRA_SMALL_SQUARE
from photos.settings_photos import EXTRA_SMALL_SQUARE_THUMBNAIL_WIDTH, MEDIUM_SQUARE_THUMBNAIL_WIDTH, LARGE_SQUARE_THUMBNAIL_WIDTH, SQUARE_THUMBNAIL_WIDTH, THUMBNAIL_QUALITY
from photos.utils.image import create_thumbnail

import datetime

strptime = datetime.datetime.strptime


def create_thumbnails(photo: Photo, file: File) -> None:
    update_extra_small_square_thumbnail(photo, file)
    update_medium_square_thumbnail(photo, file)

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


def update_thumbnail(photo: Photo, file: File) -> None:
    return
