#!/bin/sh

python manage.py migrate --noinput

gunicorn core.wsgi:application --bind 0.0.0.0:8080