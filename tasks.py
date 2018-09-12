from django.contrib.auth import get_user_model
from invoke import task
import django
import json
import os


def create_superuser():
    User = get_user_model()

    with open(os.path.join('data', 'superuser.json')) as f:
        user = json.loads(f.read())

    User.objects.create_superuser(
        user['username'], user['email'], user['password'])


@task
def clean(ctx, manual=False):
    prompt = "Removing files: are you sure? (Y/N) "

    if not input(prompt).upper().startswith('Y'):
        print("Exiting.")
        return

    ctx.run("rm -f photos.db")
    ctx.run("rm -rf media/")
    ctx.run("rm -rf temp/")
    ctx.run("rm -rf photos/migrations/")

    manage = "pipenv run python manage.py"

    ctx.run(f"{manage} makemigrations photos")
    ctx.run(f"{manage} migrate")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

    if manual:
        ctx.run(f"{manage} createsuperuser")
    else:
        print("Creating superuser account.")
        create_superuser()

    print("Done!")
