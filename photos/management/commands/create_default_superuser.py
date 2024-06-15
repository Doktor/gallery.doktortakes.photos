from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

import json
import os
import sys


class Command(BaseCommand):
    help = 'Crate a superuser, and allow password to be provided'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        from django.conf import settings

        if not settings.DEBUG:
            print("error: this command can only be used in debug mode", file=sys.stderr)
            sys.exit(1)

        credentials_path = os.path.join(settings.BASE_DIR, 'config', 'superuser.json')
        User = get_user_model()

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
