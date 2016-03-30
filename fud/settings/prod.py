import requests
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

# HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

BASE_DOMAIN = 'fud.fi'

ALLOWED_HOSTS = [
    '.fud.fi',
]

# Add instance IP address to allowed hosts for load balancer health checks
EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

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

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']

DJOSER['DOMAIN'] = 'fud.fi'

EMAIL_SENDER = SESEmailSender

ADMIN_URL = r'^säätökäli/'

GOOGLE_MAPS_API_KEY = GOOGLE_MAPS_API_KEY
