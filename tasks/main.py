from django.contrib.auth import get_user_model
from invoke import task
import django
import hashlib
import json
import os
import pprint


# Task parts

manage = "pipenv run python manage.py"


def create_superuser(ctx, manual=False):
    if manual:
        ctx.run(f"{manage} createsuperuser")
    else:
        django_setup()
        User = get_user_model()

        with open(os.path.join('data', 'superuser.json')) as f:
            user = json.loads(f.read())

        User.objects.create_superuser(
            user['username'], user['email'], user['password'])


def django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()


# Tasks


@task
def celery(ctx):
    ctx.run("pipenv run celery -A core worker --loglevel=info")


@task
def build(ctx):
    print("Rebuilding stylesheets")
    with ctx.cd(os.path.join('static', 'styles')):
        ctx.run("sass --quiet --update --no-source-map --style=compressed .:.")

    print("Collecting static files")
    ctx.run(f"{manage} collectstatic --no-input")

    print("Done!")


@task(post=[build])
def full_build(ctx, manual=False):
    prompt = "Rebuilding database: are you sure? (Y/N) "

    if not input(prompt).upper().startswith('Y'):
        print("Exiting.")
        return

    print("Creating migrations and rebuilding database")
    ctx.run(f"{manage} makemigrations --no-input photos")
    ctx.run(f"{manage} migrate --no-input")

    print("Creating superuser account")
    create_superuser(ctx, manual=manual)


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
def local_path(ctx):
    django_setup()
    from django.conf import settings
    from photos.models import Photo

    with open(os.path.join(settings.BASE_DIR, 'data', 'local_path.txt')) as f:
        base = f.read().strip()

    for root, _, files in os.walk(base):
        for file in files:
            if not file.endswith('.jpg'):
                continue

            path = os.path.join(root, file)
            prefix = os.path.dirname(path)
            album = os.path.basename(prefix)

            with open(path, 'rb') as f:
                md5 = generate_md5_hash(f)

            print(album, file, md5, sep=' / ', end='')

            try:
                photo = Photo.objects.get(md5=md5)
            except Photo.DoesNotExist:
                print(' / not found')
            else:
                print(f' / {photo.pk}')

                if photo.local_path == path:
                    continue
                else:
                    photo.local_path = path
                    photo.save()


@task
def check_generated_images(ctx, file=None, fix=False):
    """Checks that every photo has a display image and square thumbnail."""
    django_setup()
    from photos.models import Photo

    photos = Photo.objects.all().only('image', 'thumbnail', 'square_thumbnail')

    issues = []

    for photo in photos:
        if fix:
            if not photo.image.name:
                print(f"Generating new display image for photo {photo.pk}")
                photo.generate_image('display_image')
                photo.save()

            if not photo.square_thumbnail.name:
                print(f"Generating new square thumbnail for photo {photo.pk}")
                photo.generate_image('square_thumbnail')
                photo.save()

        else:
            missing = []

            if not photo.image.name:
                missing.append('display image')

            if not photo.square_thumbnail.name:
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
