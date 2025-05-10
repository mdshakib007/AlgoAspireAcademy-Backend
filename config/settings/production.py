from .base import *


DEBUG = True
ALLOWED_HOSTS = [
    'algoaspire-academy.vercel.app', 
    'api-algoaspire-academy.vercel.app',
    '127.0.0.1'
]

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
