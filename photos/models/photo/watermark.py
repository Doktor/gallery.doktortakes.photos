from django.db import models

import os


WATERMARK_COLOR_BLACK = 'black'
WATERMARK_COLOR_WHITE = 'white'

WATERMARK_COLORS = (
    (WATERMARK_COLOR_BLACK, 'Black'),
    (WATERMARK_COLOR_WHITE, 'White'),
)


def get_filename(watermark: 'Watermark', filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.strip('.')

    return f"watermarks/{watermark.color}_{watermark.width}x{watermark.height}.{ext}"


class Watermark(models.Model):
    image = models.ImageField(upload_to=get_filename, width_field='width', height_field='height')

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    color = models.CharField(max_length=10, choices=WATERMARK_COLORS)

    # Bookkeeping
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'Watermark ({self.color}, {self.width}x{self.height})'
