from fud.util.email import SESEmailSender
from .base import *
try:
    from .secrets import *
except ImportError:
    pass

DEBUG = False

SECRET_KEY = FUD_SECRET_KEY

AWS_ACCESS_KEY = AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY

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

DJOSER['DOMAIN'] = 'fud.fi'

EMAIL_SENDER = SESEmailSender
