from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.serializers import RestaurantSerializer
from .util import *

User = get_user_model()

class RestaurantApiSpec(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Restaurant.objects.all().delete()


    def test_validate_subdomain_existing(self):
        existing_restaurant,_ = create_restaurant('existing')
        url = '/restaurants/validate-subdomain?subdomain=' + existing_restaurant.subdomain
        response = self.client.get(url, HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Subdomain is already in use.')


    def test_validate_subdomain_new(self):
        url = '/restaurants/validate-subdomain?subdomain=new-subdomain'
        response = self.client.get(url, HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'true')


    def test_create_restaurant_logged_in(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        authenticate_requests(user, self.client)
        url = '/restaurants'
        data = restaurant_data()
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Restaurant.objects.filter(subdomain='test-restaurant').exists())
        self.assertEqual(Restaurant.objects.get(subdomain='test-restaurant').owner, user)


    def test_create_restaurant_logged_out(self):
        url = '/restaurants'
        data = restaurant_data()
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Restaurant.objects.filter(subdomain='test-restaurant').exists())


    def test_create_restaurant_subdomain_conflict(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        existing_restaurant, existing_user = create_restaurant('existing')
        authenticate_requests(user, self.client)
        url = '/restaurants'
        data = restaurant_data(subdomain=existing_restaurant.subdomain)
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertContains(response, 'Restaurant with this subdomain already exists.', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.get(subdomain=existing_restaurant.subdomain).owner, existing_user)


    def test_get_all_restaurants(self):
        restaurants = [create_restaurant('first')[0], create_restaurant('second')[0]]
        url = '/restaurants'
        response = self.client.get(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), RestaurantSerializer(restaurants, many=True).data)


    def test_get_restaurant_by_subdomain(self):
        restaurant, _ = create_restaurant('test-restaurant')
        url = '/restaurants/' + restaurant.subdomain
        response = self.client.get(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, RestaurantSerializer(restaurant).data)


    def test_get_restaurant_not_found(self):
        url = '/restaurants/' + 'restaurant'
        response = self.client.get(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_restaurant_as_owner(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant', user)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain
        restaurant.address = 'test-address'
        data = RestaurantSerializer(restaurant).data
        response = self.client.put(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.get(subdomain=restaurant.subdomain).address, 'test-address')


    def test_update_restaurant_as_other(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant')
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain
        restaurant.name = 'changed'
        data = RestaurantSerializer(restaurant).data
        response = self.client.put(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Restaurant.objects.get(subdomain=restaurant.subdomain).name, 'test-restaurant')


    def test_delete_restaurant_as_owner(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant', user)
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain
        response = self.client.delete(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Restaurant.objects.filter(subdomain=restaurant.subdomain).exists())


    def test_delete_restaurant_as_other(self):
        user = User.objects.create_user('test-user', 'test@example.com', 'password')
        restaurant,_ = create_restaurant('test-restaurant')
        authenticate_requests(user, self.client)
        url = '/restaurants/' + restaurant.subdomain
        response = self.client.delete(url, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Restaurant.objects.filter(subdomain=restaurant.subdomain).exists())
