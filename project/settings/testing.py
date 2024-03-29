# Tests are performed on a test_ database, however to avoid any connections/queries going to
# another database we also set this as the 'default' as well

from .base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgis",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "test_gardenserver_django"),
        "USER": "postgres",
        "PASSWORD": "password",
        "PORT": "5432",
        "HOST": "localhost",
    },
}
DATABASES["default"]["TEST"] = {"NAME": DATABASES["default"]["NAME"]}

SECRET_KEY = "secret"

STATIC_ROOT = "/static"

# Test Runner
# - Use XMLTestRunner for tox to output per test XML files
# - Output these to a separate directory to avoid clutter
TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DIR = "reports"
