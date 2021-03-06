import os
import random
import string

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer

from restaurants.models import Restaurant, Menu

User = get_user_model()
API_HOST = 'api.testserver'


def random_string(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for n in range(length))


def random_username():
    return 'user-' + random_string()


def random_restaurant_name():
    return 'restaurant-' + random_string().lower()


def random_title():
    return 'title-' + random_string()


def render_json(json):
    JSONRenderer().render(json).decode('utf-8')


def authenticate_requests(user, client):
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


def create_restaurant(subdomain=None, user=None):
    if user is None:
        user = User.objects.create_user(random_username(), 'test@example.com', 'password')
    if subdomain is None:
        subdomain = random_restaurant_name()
    restaurant = Restaurant(name=subdomain, subdomain=subdomain, owner=user,
                            address='10 Rockefeller Plaza', postal_code=10020,
                            city='New York City', phone_number='+358 50505050',
                            email=subdomain + '@fud.fi')
    restaurant.save()
    return restaurant, user


def create_menu(restaurant, title=None, content=None):
    if title is None:
        title = random_title()
    if content is None:
        content = MENU_CONTENT
    menu = Menu(title=title, content=content, restaurant=restaurant)
    menu.save()
    return menu


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


MENU_CONTENT = [
    {
        "name": "Starters",
        "items": [
            {
                "name": "Carrot on a Stick",
                "price": "1.50 €",
                "description": "Unsafe for consumption.",
                "allergens": ["V", "C"]
            }
        ]
    },
    {
        'name': 'Burgers',
        'items': [
            {
                'name': 'Seitan Burger',
                'price': '4.50 €',
                'description': 'Seitan, whole wheat, lettuce',
                'allergens': ['V']
            }
        ]
    }
]


def menu_data(title='Test Menu', content=None):
    if content is None:
        content = MENU_CONTENT
    return {
        'title': title,
        'content': content
    }


def in_travis():
    return 'TRAVIS' in os.environ
