#!/bin/sh
poetry install --no-root
poetry run ./manage.py makemigrations
poetry run ./manage.py import_default_email_template
poetry run ./manage.py collectstatic --no-input
poetry run ./manage.py test -v 3
