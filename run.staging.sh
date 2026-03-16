#!/bin/bash

set -e

cd /app/api/
uv run python manage.py migrate --no-input
uv run python manage.py create_default_superuser

echo "Collecting static files"
uv run python manage.py collectstatic --no-input --clear
echo "Successfully collected static files"

uv run gunicorn photos.wsgi -c /app/build/gunicorn.conf.py
