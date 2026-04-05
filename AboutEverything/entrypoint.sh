#!/bin/sh

python manage.py makemigrations

python manage.py migrate

python contries.py

exec python manage.py runserver