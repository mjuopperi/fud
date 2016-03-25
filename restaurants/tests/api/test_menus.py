from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.serializers import MenuSerializer
from restaurants.tests.util import *

User = get_user_model()


class MenuApiSpec(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        Menu.objects.all().delete()

    def test_create_menu_for_own_restaurant(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant', user)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/'
        data = menu_data('À la carte')
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.filter(restaurant=restaurant).count(), 1)
        menu = Menu.objects.get(restaurant=restaurant)
        self.assertEqual(menu.restaurant, restaurant)
        self.assertEqual(menu.title, 'À la carte')
        self.assertEqual(render_json(menu.content), render_json(MENU_CONTENT))

    def test_create_menu_for_other_restaurant(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant')
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/'
        data = menu_data('À la carte')
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Menu.objects.filter(restaurant=restaurant).count(), 0)

    def test_get_all_menus_of_restaurant(self):
        restaurant,_ = create_restaurant('test-restaurant')
        menus = [create_menu(restaurant), create_menu(restaurant)]
        url = '/restaurants/' + restaurant.subdomain + '/menus'
        response = self.client.get(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('menus'), MenuSerializer(menus, many=True).data)

    def test_get_menu_by_id(self):
        restaurant,_ = create_restaurant('test-restaurant')
        menu = create_menu(restaurant)
        url = '/restaurants/' + restaurant.subdomain + '/menus/' + str(menu.id)
        response = self.client.get(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MenuSerializer(menu).data)

    def test_update_menu_as_owner(self):
        restaurant, user = create_restaurant('test-restaurant')
        menu = create_menu(restaurant)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/' + str(menu.id)
        menu.title = 'changed'
        data = MenuSerializer(menu).data
        response = self.client.put(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.get(id=menu.id).title, 'changed')

    def test_update_menu_as_other(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant')
        menu = create_menu(restaurant, 'original-title')
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/' + str(menu.id)
        menu.title = 'changed'
        data = MenuSerializer(menu).data
        response = self.client.put(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Menu.objects.get(id=menu.id).title, 'original-title')

    def test_delete_menu_as_owner(self):
        restaurant, user = create_restaurant('test-restaurant')
        menu = create_menu(restaurant)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/' + str(menu.id)
        response = self.client.delete(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=menu.id).exists())

    def test_delete_menu_as_other(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant')
        menu = create_menu(restaurant)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain + '/menus/' + str(menu.id)
        response = self.client.delete(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Menu.objects.filter(id=menu.id).exists())
