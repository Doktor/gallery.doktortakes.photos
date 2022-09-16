from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

import uuid


THUMBNAIL_DISPLAY = 'display'
THUMBNAIL_EXTRA_SMALL_SQUARE = 'square_xs'
THUMBNAIL_SMALL_SQUARE = 'square'
THUMBNAIL_MEDIUM_SQUARE = 'square_md'
THUMBNAIL_LARGE_SQUARE = 'square_lg'

THUMBNAIL_MEDIUM = 'display_md'

# Deprecated
THUMBNAIL_COVER = 'cover'


THUMBNAIL_TYPES = (
    (THUMBNAIL_DISPLAY, 'Display'),
    (THUMBNAIL_EXTRA_SMALL_SQUARE, 'Square (extra small)'),
    (THUMBNAIL_SMALL_SQUARE, 'Square (small)'),
    (THUMBNAIL_MEDIUM_SQUARE, 'Square (medium)'),
    (THUMBNAIL_LARGE_SQUARE, 'Square (large)'),

    (THUMBNAIL_MEDIUM, 'Regular (medium)'),

    # Deprecated
    (THUMBNAIL_COVER, 'Cover'),
)


def get_filename(thumbnail: 'Thumbnail', filename: str) -> str:
    datetime = thumbnail.photo.taken.strftime("%Y%m%d_%H%M%S")
    identifier = thumbnail.photo.short_md5
    suffix = uuid.uuid4().hex[0:8]

    return f"images/{datetime}_{identifier}_{suffix}.jpg"


class Thumbnail(models.Model):
    photo = models.ForeignKey("Photo", on_delete=models.CASCADE, related_name='thumbnails')
    type = models.CharField(max_length=10, choices=THUMBNAIL_TYPES, blank=True)

    # Image

    image = models.ImageField(
        upload_to=get_filename,
        width_field='width',
        height_field='height',
        blank=True,
        null=True,
        editable=False)
    is_watermarked = models.BooleanField(default=False)

    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    file_size = models.CharField(max_length=50, editable=False, blank=True)

    # Bookkeeping

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'Thumbnail for photo {self.photo_id} ({self.width}x{self.height})'


@receiver(post_delete, sender=Thumbnail,
          dispatch_uid='receiver_delete_thumbnail_image')
def receiver_delete_thumbnail_image(sender, instance: Thumbnail, **kwargs) -> None:
    instance.image.delete(save=False)
