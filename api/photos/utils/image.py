from django.core.files import File

from photos.models import Photo, Thumbnail
from photos.utils.models import format_file_size

from io import BytesIO
from typing import List, Tuple
import PIL.Image


def int_all(*nums: float) -> List[int]:
    return [int(n) for n in nums]


def create_thumbnail(
        photo: Photo,
        file: File,
        width: int,
        height: int,
        name: str,
        quality: int = 90) -> "Thumbnail":

    image = PIL.Image.open(file)

    exif = image.info.get('exif', None)
    icc_profile = image.info.get('icc_profile', None)

    try:
        thumbnail = Thumbnail.objects.get(photo=photo, width=width, height=height)
        thumbnail.image.delete(save=False)
    except Thumbnail.DoesNotExist:
        thumbnail = Thumbnail()

    thumbnail.photo = photo
    thumbnail.type = name

    if image.size != (width, height):
        image = fit_image(image, (width, height))

    assert image.width == width
    assert image.height == height

    data = BytesIO()
    image.save(data, 'JPEG', quality=quality, exif=exif, icc_profile=icc_profile)

    new_file = File(data)

    thumbnail.file_size = format_file_size(new_file.size)

    thumbnail.image.save(photo.filename, new_file, save=False)
    thumbnail.save()
    return thumbnail


def fit_image(image: PIL.Image, size: Tuple[int, int]) -> PIL.Image:
    """Resizes an image so that it fits within the given long_size, without
    distorting the image and cropping the sides as necessary."""
    if image.format != 'JPEG':
        image = image.convert('RGB')

    old_w, old_h = image.size
    old_ratio = old_w / old_h

    new_w, new_h = size
    new_ratio = new_w / new_h

    # Original image is too tall, crop top and bottom
    # Portrait -> landscape
    if new_ratio > old_ratio:
        scale = new_w / old_w
        new_h = new_h / scale

        top = (old_h - new_h) / 2
        bottom = top + new_h

        image = image.crop(int_all(0, top, old_w, bottom))

    # Original image is too wide, crop left and right
    # Landscape -> portrait
    elif new_ratio < old_ratio:
        scale = new_h / old_h
        new_w = new_w / scale

        left = (old_w - new_w) / 2
        right = left + new_w

        image = image.crop(int_all(left, 0, right, old_h))

    return image.resize(size, PIL.Image.LANCZOS)
