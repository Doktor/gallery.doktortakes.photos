from django.contrib.auth import get_user_model
from invoke import task
import django
import json
import os


# Task parts


manage = "pipenv run python manage.py"


def create_superuser(ctx, manual=False):
    if manual:
        ctx.run(f"{manage} createsuperuser")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        django.setup()

        User = get_user_model()

        with open(os.path.join('data', 'superuser.json')) as f:
            user = json.loads(f.read())

        User.objects.create_superuser(
            user['username'], user['email'], user['password'])


# Tasks


@task
def build(ctx, manual=False):
    print("Creating migrations and rebuilding database")
    ctx.run(f"{manage} makemigrations --no-input photos")
    ctx.run(f"{manage} migrate --no-input")

    print("Creating superuser account")
    create_superuser(ctx, manual=manual)

    print("Rebuilding stylesheets")
    with ctx.cd(os.path.join('static', 'styles')):
        ctx.run("sass --update .:.")

    print("Collecting static files")
    ctx.run(f"{manage} collectstatic --no-input")

    print("Done!")


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
