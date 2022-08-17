from django.core.files import File

from photos.models import Photo, Thumbnail, Watermark
from photos.settings_photos import WATERMARK_OFFSET_PERCENT
from photos.utils.models import format_file_size

from io import BytesIO
from typing import List, Optional, Tuple
import PIL.Image


def int_all(*nums: float) -> List[int]:
    return [int(n) for n in nums]


def create_thumbnail(
        photo: Photo,
        file: File,
        width: int,
        height: int,
        name: str,
        quality: int = 90,
        add_watermark: bool = False,
        watermark_color: str = None) -> "Thumbnail":

    image = PIL.Image.open(file)

    exif = image.info.get('exif', None)
    icc_profile = image.info.get('icc_profile', None)

    try:
        thumbnail = Thumbnail.objects.get(photo=photo, width=width, height=height, is_watermarked=add_watermark)
        thumbnail.image.delete(save=False)
    except Thumbnail.DoesNotExist:
        thumbnail = Thumbnail()

    thumbnail.photo = photo
    thumbnail.type = name

    if image.size != (width, height):
        image = fit_image(image, (width, height))

    if add_watermark:
        thumbnail.is_watermarked = True
        image = apply_watermark(image, watermark_color)

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
    """Resizes an image so that it fits within the given size, without
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


def apply_watermark(image: PIL.Image, color: str) -> PIL.Image:
    """Applies a watermark to an image."""
    w, h = image.size
    image_size = max(w, h)

    try:
        watermark = Watermark.objects.get(apply_to_size=image_size, color=color)
    except Watermark.DoesNotExist:
        raise RuntimeError(f"no watermark found for parameters: size = {image_size}, color = {color}")

    watermark_image = PIL.Image.open(watermark.image)

    offset = int(image_size * (WATERMARK_OFFSET_PERCENT / 100))

    x = w - watermark_image.width - offset
    y = h - watermark_image.height - offset
    coords = (x, y)

    image.paste(watermark_image, coords, mask=watermark_image.split()[3])
    return image


RATIOS = [(1, 1), (3, 2), (4, 3), (5, 4), (16, 9), (16, 10), (2.35, 1), (2.39, 1)]
TOLERANCE = 1 / 100


def guess_aspect_ratio(w: int, h: int) -> float:
    long, short = max(w, h), min(w, h)

    for rl, rs in RATIOS:
        ratio = rl / rs

        if abs((long / short) - ratio) < TOLERANCE:
            if w > h:
                return ratio
            else:
                return 1 / ratio
    else:
        return w / h
