from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

import re

RESERVED_SUBDOMAINS = [
    'static',
    'api',
    'fud',
]

SUBDOMAIN_PATTERN = re.compile("^[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?$")


def validate_subdomain(subdomain):
    if subdomain in RESERVED_SUBDOMAINS:
        raise ValidationError('The subdomain "%s" is reserved' % subdomain)
    if SUBDOMAIN_PATTERN.match(subdomain) is None:
        raise ValidationError('Allowed characters: a-z, 0-9 and -')
    if subdomain.startswith('www'):
        raise ValidationError('Subdomains starting with www* are not allowed')


class Restaurant(models.Model):
    name = models.TextField()
    subdomain = models.TextField(unique=True, validators=[validate_subdomain], db_index=True)
    address = models.TextField(null=True, blank=True, default=None)
    postal_code = models.TextField(null=True, blank=True, default=None)
    city = models.TextField(null=True, blank=True, default=None)
    phone_number = models.TextField(null=True, blank=True, default=None)
    email = models.TextField(null=True, blank=True, default=None)
    owner = models.ForeignKey(User)

    class Meta:
        db_table = 'restaurant'

    def __str__(self):
        return u'%s' % (self.name,)


class Menu(models.Model):
    title = models.TextField()
    content = JSONField()
    restaurant = models.ForeignKey(Restaurant)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu'
