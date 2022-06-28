# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log


RUN mkdir -p /opt/app
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements/production.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM

RUN python manage.py collectstatic --noinput --clear --settings project.settings.static
CMD ["/opt/app/start_server.sh"]