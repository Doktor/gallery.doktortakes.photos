from photos.settings import DEFAULT_WATERMARK, WATERMARK_IMAGES, WATERMARK_OFFSET

import PIL.Image
from typing import Tuple, Iterator


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
