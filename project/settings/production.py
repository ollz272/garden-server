from .base import *

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST', '').split(' ')

CSRF_TRUSTED_ORIGINS = [f"http://{host}" for host in os.environ.get('ALLOWED_HOST', '').split(' ')]
SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get("DEBUG"):
    DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "gardenserver_django"),
        "USER": os.environ.get("DJANGO_DATABASE_USER"),
        "PASSWORD":  os.environ.get("DJANGO_DATABASE_PASSWORD"),
        "PORT": "5432",
        "HOST":  os.environ.get("DJANGO_DATABASE_HOST"),
    },
}