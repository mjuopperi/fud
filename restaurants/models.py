from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import re

NOT_ALLOWED_SUBDOMAINS = [
    'static',
    'api',
    'fud',
]

SUBDOMAIN_PATTERN = re.compile("^[a-z0-9][a-z0-9\-][a-z0-9]*$")


def validate_subdomain(subdomain):
    if subdomain in NOT_ALLOWED_SUBDOMAINS:
        raise ValidationError('%s is not allowed subdomain' % subdomain)
    if SUBDOMAIN_PATTERN.match(subdomain) is None:
        raise ValidationError('Allowed characters: a-z, 0-9 and -, only lowercase')
    if subdomain.startswith('www'):
        raise ValidationError('Subdomain starting with www* is not allowed')


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=30, unique=True, validators=[validate_subdomain])
    address = models.CharField(max_length=255, null=True, blank=True, default=None)
    postal_code = models.CharField(max_length=5, null=True, blank=True, default=None)
    city = models.CharField(max_length=45, null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=32, null=True, blank=True, default=None)
    email = models.EmailField()
    owner = models.ForeignKey(User)

    def __str__(self):
        return u'%s' % (self.name,)


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=80)

    def __str__(self):
        return u'%s' % (self.name,)


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    allergies = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return u'%s' % (self.title,)
