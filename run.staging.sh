#!/bin/bash

set -e

cd /app/api/
poetry run python manage.py migrate --no-input
poetry run python manage.py create_default_superuser

echo "Collecting static files"
poetry run python manage.py collectstatic --no-input --clear
echo "Successfully collected static files"

poetry run gunicorn photos.wsgi -c /app/build/gunicorn.conf.py
