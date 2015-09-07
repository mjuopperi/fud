from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fud_test',
        'USER': 'fuduser',
        'PASSWORD': 'kugganen',
        'HOST': '192.168.33.10',
        'PORT': '5432',
    }
}
