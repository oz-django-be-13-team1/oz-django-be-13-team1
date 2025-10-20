#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE="config.settings.prod"
uv run python manage.py makemigrations --check --noinput
uv run python manage.py migrate
uv run gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2