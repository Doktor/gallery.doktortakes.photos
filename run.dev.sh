#!/bin/bash
poetry run python manage.py migrate --no-input
poetry run inv create-default-superuser
poetry run python manage.py runserver 0.0.0.0:8000
