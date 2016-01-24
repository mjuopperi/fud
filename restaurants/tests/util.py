import random
import string

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from restaurants.models import Restaurant

User = get_user_model()
API_HOST = 'api.testserver'

def random_string(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for n in range(length))

def random_username():
    return 'user-' + random_string()

def authenticate_requests(user, client):
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


def create_restaurant(subdomain, user=None):
    if user == None:
        user = User.objects.create_user(random_username(), 'test@example.com', 'password')
    restaurant = Restaurant(name=subdomain, subdomain=subdomain, owner=user)
    restaurant.save()
    return (restaurant, user)


def signup_data(username='test-user', email='test@example.com', password='password'):
    return {
        'username': username,
        'email': email,
        'password': password
    }


def restaurant_data(name='Test Restaurant', subdomain='test-restaurant', address='',
                    postal_code='', city='', phone_number='', email=''):
    return {
        'name': name,
        'subdomain': subdomain,
        'address': address,
        'postal_code': postal_code,
        'city': city,
        'phone_number': phone_number,
        'email': email
    }
