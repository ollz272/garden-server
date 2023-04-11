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

# Cache pages to a bare minimum to ensure decent performance under high load
MIDDLEWARE = (
    [
        "cookiefilter.middleware.CookieFilterMiddleware",
        "django.middleware.cache.UpdateCacheMiddleware",
    ]
    + MIDDLEWARE
    + ["django.middleware.cache.FetchFromCacheMiddleware"]
)
CACHE_MIDDLEWARE_SECONDS = 30
