# syntax=docker/dockerfile:1
FROM python:3.11-bullseye
RUN apt-get update && apt-get install nginx=1.23.4 -y --no-install-recommends  && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir /app
WORKDIR /app

RUN pip install --no-cache-dir poetry==1.4.2 && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml README.md /app/

# to prevent poetry from installing my actual app,
# and keep docker able to cache layers
RUN mkdir -p /app/src/app && touch /app/src/app/__init__.py && poetry install -n

# now actually copy the real contents of my app
COPY . /app/src/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
WORKDIR /app/src/app

RUN python manage.py collectstatic --noinput --clear --settings project.settings.static
CMD ["/app/src/app/start_server.sh"]