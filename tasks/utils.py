from typing import Optional

from django.db.models.fields.files import ImageFieldFile


def generate_image(photo: "Photo", image_type: str, save: bool = False) -> None:
    from photos.tasks import update_display_image, update_thumbnail, update_square_thumbnail

    file = photo.get_original()

    if image_type == 'display_image':
        function = update_display_image
    elif image_type == 'thumbnail':
        function = update_thumbnail
    elif image_type == 'square_thumbnail':
        function = update_square_thumbnail
    else:
        return

    function(photo, file)

    if save:
        photo.save()


def get_image_file(photo: "Photo", image_type: str) -> Optional[ImageFieldFile]:
    from photos.models.photo.thumbnail import THUMBNAIL_COVER, THUMBNAIL_DISPLAY, THUMBNAIL_SMALL_SQUARE

    if image_type == 'original':
        return photo.original
    elif image_type == 'display_image':
        thumbnail = photo.get_thumbnail(THUMBNAIL_DISPLAY)
    elif image_type == 'square_thumbnail':
        thumbnail = photo.get_thumbnail(THUMBNAIL_SMALL_SQUARE)
    elif image_type == 'thumbnail':
        thumbnail = photo.get_thumbnail(THUMBNAIL_COVER)
    else:
        raise ValueError

    return thumbnail.image if thumbnail else None


def get_image_filename(photo: "Photo", image_type: str) -> Optional[str]:
    file = get_image_file(photo, image_type)
    return file.name if file is not None else None
