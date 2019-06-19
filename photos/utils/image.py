import PIL.Image
from typing import Tuple, Iterator


def round_all(*nums: float) -> Iterator[int]:
    return (int(round(n)) for n in nums)


def thumbnail(image: PIL.Image, size: Tuple[int, int]) -> PIL.Image:
    original_w, original_h = image.size
    original_ratio = original_w / original_h

    target_w, target_h = size
    target_ratio = target_w / target_h

    # Too tall: crop top/bottom
    if target_ratio > original_ratio:
        scale = target_w / original_w
        new_h = target_h / scale

        top = (original_h - new_h) / 2
        bottom = top + new_h

        image = image.crop(round_all(0, top, original_w, bottom))

    # Too wide: crop left/right
    elif target_ratio < original_ratio:
        scale = target_h / original_h
        new_w = target_w / scale

        left = (original_w - new_w) / 2
        right = left + new_w

        image = image.crop(round_all(left, 0, right, original_h))

    return image.resize(size, PIL.Image.LANCZOS)
