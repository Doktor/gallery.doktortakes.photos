#!/bin/bash

set -e

cd /app/api/

echo "Collecting static files"
poetry run python manage.py collectstatic --no-input --clear
echo "Successfully collected static files"

poetry run gunicorn photos.wsgi -c /app/build/gunicorn.conf.py
