#!/bin/bash
echo "Collecting static files"
poetry run python manage.py collectstatic --no-input --clear
echo "Successfully collected static files"

poetry run celery -A photos worker --loglevel=INFO
