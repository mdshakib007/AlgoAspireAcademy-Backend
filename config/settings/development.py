# config/settings/development.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

FRONTEND_URL = 'http://localhost:3000'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}