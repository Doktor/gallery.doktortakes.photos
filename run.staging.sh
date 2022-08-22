#!/bin/bash

set -e

poetry run python manage.py migrate --no-input
poetry run inv create-default-superuser

echo "Collecting static files"
poetry run python manage.py collectstatic --no-input --clear
echo "Successfully collected static files"

poetry run gunicorn photos.wsgi -c ./build/gunicorn.conf.py
