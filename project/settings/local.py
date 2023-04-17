from .base import *

DEBUG = True
INTERNAL_IPS = ["127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1"]
ALLOWED_HOSTS = ["*"]

SECRET_KEY = "gardenserver"

DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgis",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "gardenserver_django"),
        "USER": "",
        "PASSWORD": "",
        "PORT": "5432",
        "HOST": "",
    },
}

# Django debug toolbar - show locally unless DISABLE_TOOLBAR is enabled with environment vars
# eg. DISABLE_TOOLBAR=1 ./manage.py runserver
if not os.environ.get("DISABLE_TOOLBAR"):
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
