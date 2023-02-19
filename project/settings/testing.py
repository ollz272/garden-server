# Tests are performed on a test_ database, however to avoid any connections/queries going to
# another database we also set this as the 'default' as well
DATABASES = {"default": dj_database_url.config(default="postgis:///test_acts435_django")}
DATABASES["default"]["TEST"] = {"NAME": DATABASES["default"]["NAME"]}

SECRET_KEY = "secret"

STATIC_ROOT = os.environ["STATIC_ROOT"]

INSTALLED_APPS += ["django_extensions"]

# Test Runner
# - Use XMLTestRunner for tox to output per test XML files
# - Output these to a separate directory to avoid clutter
TEST_RUNNER = "core.test_runners.XMLTestRunner"
TEST_OUTPUT_DIR = "reports"