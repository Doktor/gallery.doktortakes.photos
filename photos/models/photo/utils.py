from django.core.exceptions import ValidationError
from django.core.files import File

from photos.models.utils import DATE_FORMAT, get_modified_time_utc
from photos.settings import (
    DEFAULT_WATERMARK, WATERMARK_IMAGES, WATERMARK_OFFSET,
    COLOR_NONE, COLOR_WHITE, COLOR_BLACK,
    CHECK_MINIMUM_SIZE, MINIMUM_LONG_EDGE, MINIMUM_SHORT_EDGE)

import datetime
import exifread
import PIL.Image
import pytz
from lxml import etree
from typing import Tuple, Iterator


strptime = datetime.datetime.strptime

XMP_START = b'<x:xmpmeta'
XMP_END = b'</x:xmpmeta>'

NS = {
    'x': "adobe:ns:meta/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'xmp': "http://ns.adobe.com/xap/1.0/"
}

IMAGE_TYPES = ['original', 'display_image', 'square_thumbnail', 'thumbnail']


def int_all(*nums: float) -> Iterator[int]:
    return (int(n) for n in nums)


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


def fit_image_long_edge(image: PIL.Image, new_long: int) -> PIL.Image:
    """Creates a thumbnail of an image given the size of the long edge."""
    w, h = image.size

    long, short = max(w, h), min(w, h)
    new_short = int(short / long * new_long)

    if w >= h:
        size = (new_long, new_short)
    else:
        size = (new_short, new_long)

    return fit_image(image, size)


def apply_watermark(image: PIL.Image, color: str) -> PIL.Image:
    """Applies a watermark to an image."""
    w, h = image.size
    size = max(w, h)

    watermark = WATERMARK_IMAGES.get((size, color), DEFAULT_WATERMARK)
    offset = int(WATERMARK_OFFSET * (size / 2400))

    x = w - watermark.size[0] - offset
    y = h - watermark.size[1] - offset
    coords = (x, y)

    image.paste(watermark, coords, mask=watermark.split()[3])
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


def check_dimensions(file: File) -> None:
    """Checks the dimensions of an uploaded image and raises a ValidationError
    if the image is too small."""

    if not CHECK_MINIMUM_SIZE:
        return

    image = PIL.Image.open(file)
    long, short = max(*image.size), min(*image.size)

    if long < MINIMUM_LONG_EDGE or short < MINIMUM_SHORT_EDGE:
        raise ValidationError(
            "The uploaded image is too small: the minimum size is "
            f"{MINIMUM_LONG_EDGE}x{MINIMUM_SHORT_EDGE} px, "
            f"but the uploaded image was {long}x{short} px.")


def parse_exif_data(photo: 'Photo', file: File) -> None:
    """Extracts EXIF data from an image and adds it to a Photo object."""

    file.seek(0)
    raw_exif = exifread.process_file(file, details=False, debug=False)
    photo.exif = {k: v.printable for k, v in raw_exif.items()}

    # Timestamps
    modified = get_modified_time_utc(file)
    tz = pytz.utc

    taken = photo.exif.get('EXIF DateTimeOriginal', None)
    if taken is not None:
        photo.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.taken = modified

    edited = photo.exif.get('Image DateTime', None)
    if edited is not None:
        photo.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.edited = modified


def parse_xmp_data(photo: 'Photo', file: File) -> None:
    """Extracts XMP data from an image and adds it to a Photo object."""

    file.seek(0)
    data = file.read()
    start = data.find(XMP_START)
    end = data.find(XMP_END)

    if start == -1 or end == -1:
        pass
    else:
        xml = data[start:end + len(XMP_END)].decode('utf-8')
        root = etree.fromstring(xml)

        element = root.xpath('.//rdf:Description', namespaces=NS)[0]

        try:
            rating = element.xpath('@xmp:Rating', namespaces=NS)[0]
            photo.rating = int(rating)
        except IndexError:
            photo.rating = 0

        try:
            label = element.xpath('@xmp:Label', namespaces=NS)[0].lower()
        except IndexError:
            photo.watermark = COLOR_NONE
        else:
            photo.watermark = \
                (COLOR_BLACK if label == 'green' else COLOR_WHITE)


def format_f_stop(f: str) -> float:
    """Takes an f-stop as a fractional string and converts it to a number."""
    try:
        f = f.split('/')
    except AttributeError:
        return 0
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return float(f[0])


def get_exif(photo: 'Photo') -> dict:
    e = photo.exif

    camera = e.get('Image Model', 'Camera unknown')

    try:
        make = e.get('EXIF LensMake', e['Image Make'])
        model = e['EXIF LensModel']

        lens = f'{make} {model}'
    except KeyError:
        lens = 'Lens unknown'

    if 'EF-S' in lens:
        lens = lens.replace('EF-S', 'EF-S ')
    elif 'EF' in lens:
        lens = lens.replace('EF', 'EF ')

    try:
        focal_length = f"{e['EXIF FocalLength']} mm"
    except KeyError:
        focal_length = 'Unknown'

    try:
        shutter_speed = f"{e['EXIF ExposureTime']} s"
    except KeyError:
        shutter_speed = 'Unknown'

    try:
        f_stop = f"f/{format_f_stop(e['EXIF FNumber'])}"
    except KeyError:
        if camera != 'Camera unknown':
            f_stop = 'f/0'
        else:
            f_stop = 'Unknown'

    try:
        iso_speed = f"ISO {e['EXIF ISOSpeedRatings']}"
    except KeyError:
        iso_speed = 'Unknown'

    return {
        'camera': camera,
        'lens': lens,
        'focal_length': focal_length,
        'shutter_speed': shutter_speed,
        'aperture': f_stop,
        'iso_speed': iso_speed,
    }
