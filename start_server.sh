#!/usr/bin/env bash
echo "Migrating.."
./manage.py migrate --settings="project.settings.production"

echo "Collect static..."
./manage.py collectstatic --noinput --clear --settings project.settings.production

# start-server.sh
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (./manage.py createsuperuser --no-input --email $DJANGO_SUPERUSER_EMAIL )
fi
(gunicorn project.wsgi --user www-data --bind 0.0.0.0:8020 --workers 1)
