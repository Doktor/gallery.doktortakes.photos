import sys

from django.contrib.auth import get_user_model
from invoke import task
import datetime
import django
import hashlib
import json
import os
import pprint
import pytz
import shlex
import subprocess

from models.photo.thumbnail import THUMBNAIL_DISPLAY, THUMBNAIL_SMALL_SQUARE
from .utils import generate_image


# Task parts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

manage = "pipenv run python manage.py"


def check_output(command: str) -> str:
    return subprocess.run(
        shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True).stdout


@task
def create_default_superuser(ctx):
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

    User.objects.create_superuser(
        user['username'], user['email'], user['password'])


def django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photos.settings_django")
    django.setup()


# Tasks


@task()
def full_build(ctx):
    prompt = "Rebuilding database: are you sure? (Y/N) "

    if not input(prompt).upper().startswith('Y'):
        print("Exiting.")
        return

    print("Creating migrations and rebuilding database")
    ctx.run(f"{manage} makemigrations --no-input photos")
    ctx.run(f"{manage} migrate --no-input")


@task
def clean(ctx):
    prompt = "Removing files: are you sure? (Y/N) "

    if not input(prompt).upper().startswith('Y'):
        print("Exiting.")
        return

    ctx.run("rm -f photos.db")
    ctx.run("rm -rf media/")
    ctx.run("rm -rf temp/")
    ctx.run("rm -rf photos/migrations/")

    with ctx.cd(os.path.join('static', 'styles')):
        ctx.run("rm -rf .sass-cache/")
        ctx.run("rm -f *.css")
        ctx.run("rm -f *.css.map")

    print("Done!")


def generate_md5_hash(file):
    hasher = hashlib.md5()

    while True:
        data = file.read(1024 ** 2)
        if not data:
            break
        hasher.update(data)

    return hasher.hexdigest()


@task
def check_generated_images(ctx, file=None, fix=False):
    """Checks that every photo has a display image and square thumbnail."""
    django_setup()
    from photos.models import Photo

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
