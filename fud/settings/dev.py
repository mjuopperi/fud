from .base import *

DEBUG = True

BASE_DOMAIN = 'fud.localhost'

ALLOWED_HOSTS = {
    '.fud.localhost',
}

MIDDLEWARE_CLASSES = (
    'fud.util.middleware.LocalhostRedirectionMiddleware',
) + MIDDLEWARE_CLASSES

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fud',
        'USER': 'fuduser',
        'PASSWORD': 'kugganen',
        'HOST': '192.168.33.10',
        'PORT': '5432',
    }
}
