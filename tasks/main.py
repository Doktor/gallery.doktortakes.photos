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


# Task parts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

manage = "pipenv run python manage.py"


def check_output(command: str) -> str:
    return subprocess.run(
        shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True).stdout


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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photos.settings_django")
    django.setup()


# Tasks


@task
def git_status(ctx):
    def get_last_commit_datetime():
        raw = check_output("git log -1 --format=%at").strip()
        utc = datetime.datetime.utcfromtimestamp(int(raw)).replace(tzinfo=pytz.utc)
        local = utc.astimezone(pytz.timezone('US/Eastern'))

        return local.strftime('%Y-%m-%d %H:%M:%S')

    def get_last_commit_hash():
        return check_output("git log -1 --format=%H").strip()

    def get_last_20_commits():
        raw = check_output("git log --max-count=20 --format=\"%H %s\"").strip()
        lines = [line.split(' ', 1) for line in raw.split('\n')]

        return [{'hash': line[0], 'subject': line[1]} for line in lines]

    data = {
        'commit_list': "https://gitlab.com/Doktor/doktortakes.photos/commits/master",
        'commit_link': "https://gitlab.com/Doktor/doktortakes.photos/commit/",
        'last_commit_datetime': get_last_commit_datetime(),
        'last_commit_hash': get_last_commit_hash(),
        'last_20_commits': get_last_20_commits(),
    }

    with open('data/git.json', 'w') as f:
        f.write(json.dumps(data))


@task
def build(ctx):
    print("Generating Git status file")
    git_status(ctx)

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
