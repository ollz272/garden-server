from .base import *

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST', '').split(' ')
DEBUG= True
#CSRF_TRUSTED_ORIGINS = [f"http://{os.environ.get('ALLOWED_HOST', '').split(' ')}"]
SECRET_KEY = 'gardenserver'