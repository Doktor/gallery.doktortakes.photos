from typing import Optional

from django.db.models.fields.files import ImageFieldFile

from photos.models.photo import Photo, get_display_path, get_original_path, get_square_thumbnail_path, get_thumbnail_path


def generate_image(photo: Photo, image_type: str, save: bool = False) -> None:
    file = photo.get_original()

    if image_type == 'display_image':
        from photos.tasks import update_display_image
        function = update_display_image
    elif image_type == 'thumbnail':
        from photos.tasks import update_thumbnail
        function = update_thumbnail
    elif image_type == 'square_thumbnail':
        from photos.tasks import update_square_thumbnail
        function = update_square_thumbnail
    else:
        return

    function(photo, file)

    if save:
        photo.save()


def get_image_file(photo: Photo, image_type: str) -> Optional[ImageFieldFile]:
    if image_type == 'original':
        return photo.original
    elif image_type == 'display_image':
        return photo.image
    elif image_type == 'square_thumbnail':
        return photo.square_thumbnail
    elif image_type == 'thumbnail':
        return photo.thumbnail
    else:
        raise ValueError


def get_image_filename(photo: Photo, image_type: str) -> Optional[str]:
    file = get_image_file(photo, image_type)
    return file.name if file is not None else None


def get_image_filename_candidate(photo: Photo, image_type: str) -> Optional[str]:
    if image_type == 'original':
        function = get_original_path
    elif image_type == 'display_image':
        function = get_display_path
    elif image_type == 'square_thumbnail':
        function = get_square_thumbnail_path
    elif image_type == 'thumbnail':
        function = get_thumbnail_path
    else:
        raise ValueError

    filename = get_image_filename(photo, image_type)
    return function(photo, filename) if filename is not None else None
