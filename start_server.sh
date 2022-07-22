#!/usr/bin/env bash
echo "Migrating.."
python manage.py migrate


# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(gunicorn project.wsgi --user www-data --bind 0.0.0.0:8010 --workers 4) &
nginx -g "daemon off;"