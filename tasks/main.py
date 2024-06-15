from django.contrib.auth import get_user_model
import django
import json
import os
import pprint
import shlex
import subprocess
import sys


# Task parts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_output(command: str) -> str:
    return subprocess.run(
        shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True).stdout


def create_default_superuser():
    django_setup()
    User = get_user_model()

    from django.conf import settings

    if not settings.DEBUG:
        print("error: this script can only be used in debug mode", file=sys.stderr)
        sys.exit(1)

    credentials_path = os.path.join(BASE_DIR, 'config', 'superuser.json')

    try:
        with open(credentials_path) as f:
            user = json.loads(f.read())
    except FileNotFoundError:
        print("error: credentials file not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("error: failed to decode credentials file")
        sys.exit(1)

    if User.objects.filter(is_superuser=True).exists():
        print("warning: a default superuser already exists")
        sys.exit(0)
    User.objects.create_superuser(
        user['username'], user['email'], user['password'])


def django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photos.settings_django")
    django.setup()


# Tasks


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
