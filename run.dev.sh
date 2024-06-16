#!/bin/bash

set -e

cd /app/api/
poetry run python manage.py migrate --no-input
poetry run python manage.py create_default_superuser
poetry run python manage.py runserver 0.0.0.0:8000
