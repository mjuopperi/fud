from .base import *
try:
    from .secrets import *
except ImportError:
    pass

DEBUG = False

SECRET_KEY = FUD_SECRET_KEY

BASE_DOMAIN = 'fud.fi'

ALLOWED_HOSTS = {
    '*',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fud',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

STATIC_ROOT = '/home/fud/server/static/'
