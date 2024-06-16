from photos.management.commands.archive.utils import django_setup

import pprint


def check_generated_images(file=None, fix=False):
    """Checks that every photo has a display image and square thumbnail."""
    django_setup()

    from photos.models import Photo
    from photos.models.photo.thumbnail import THUMBNAIL_DISPLAY, THUMBNAIL_SMALL_SQUARE
    from .utils import generate_image

    photos = Photo.objects.all()

    issues = []

    for photo in photos:
        if fix:
            if not photo.get_thumbnail(THUMBNAIL_DISPLAY):
                print(f"Generating new display image for photo {photo.pk}")
                generate_image(photo, 'display_image')
                photo.save()

            if not photo.get_thumbnail(THUMBNAIL_SMALL_SQUARE):
                print(f"Generating new square thumbnail for photo {photo.pk}")
                generate_image(photo, 'square_thumbnail')
                photo.save()

        else:
            missing = []

            if not photo.get_thumbnail(THUMBNAIL_DISPLAY):
                missing.append('display image')

            if not photo.get_thumbnail(THUMBNAIL_SMALL_SQUARE):
                missing.append('square thumbnail')

            if missing:
                issues.append({
                    'photo': photo.pk,
                    'album': photo.album.name,
                    'missing': ', '.join(missing)
                })

    if issues:
        if file is None:
            pprint.pprint(issues)
        else:
            with open(file, 'w') as f:
                f.write(pprint.pformat(issues))
