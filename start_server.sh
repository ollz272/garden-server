#!/usr/bin/env bash
echo "Migrating.."
poetry run ./manage.py migrate --settings="project.settings.production"


# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (poetry run ./manage.py createsuperuser --no-input)
fi
(poetry run gunicorn project.wsgi --user www-data --bind 0.0.0.0:8010 --workers 4) &
nginx -g "daemon off;"