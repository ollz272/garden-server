from .base import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(" ")

SECRET_KEY = os.environ.get("SECRET_KEY")

if os.environ.get("DEBUG"):
    DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": 'timescale.db.backends.postgresql',
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "gardenserver_django"),
        "USER": os.environ.get("DJANGO_DATABASE_USER"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD"),
        "PORT": "5432",
        "HOST": os.environ.get("DJANGO_DATABASE_HOST"),
    },
}


DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_ACCESS_KEY_ID = os.environ.get("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.environ.get("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "eu-west-2"
AWS_S3_ADDRESSING_STYLE = "virtual"

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
