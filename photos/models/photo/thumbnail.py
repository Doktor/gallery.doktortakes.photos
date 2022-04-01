from django.db import models


THUMBNAIL_DISPLAY = 'display'
THUMBNAIL_COVER = 'cover'
THUMBNAIL_SMALL_SQUARE = 'square'

THUMBNAIL_TYPES = (
    (THUMBNAIL_DISPLAY, 'Display'),
    (THUMBNAIL_COVER, 'Cover'),
    (THUMBNAIL_SMALL_SQUARE, 'Square'),
)


def get_filename(thumbnail: 'Thumbnail', filename: str) -> str:
    photo = thumbnail.photo
    datetime = photo.taken.strftime("%Y%m%d_%H%M%S")
    dimensions = f"{photo.width}x{photo.height}"

    return f"images/{datetime}_{photo.short_md5}_{dimensions}.jpg"


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
        return f'Thumbnail for photo {self.photo.id} ({self.width}x{self.height})'
