from .base import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(" ")

SECRET_KEY = os.environ.get("SECRET_KEY")

if os.environ.get("DEBUG"):
    DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "gardenserver_django"),
        "USER": os.environ.get("DJANGO_DATABASE_USER"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD"),
        "PORT": "5432",
        "HOST": os.environ.get("DJANGO_DATABASE_HOST"),
    },
}


# Cache sessions for optimum performance
if os.environ.get("REDIS_SERVERS"):
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"


if not os.environ.get("DISABLE_TOOLBAR"):
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1"]
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    DEBUG_TOOLBAR_CONFIG = {
        "SKIP_TEMPLATE_PREFIXES": (
            "django/forms/widgets/",
            "admin/widgets/",
            "bootstrap/",
        ),
    }
