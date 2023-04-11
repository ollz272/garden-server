# syntax=docker/dockerfile:1
FROM python:3.11-bullseye

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
EXPOSE 8000
STOPSIGNAL SIGTERM
WORKDIR /app/src/app

RUN ./manage.py collectstatic --noinput --clear --settings project.settings.production


CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "project.wsgi"]