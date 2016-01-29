from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .util import *

User = get_user_model()

class AuthApiSpec(APITestCase):
    def setUp(self):
        User.objects.create_user('existing-user', 'existing@example.com', 'password')

    def tearDown(self):
        User.objects.all().delete()

    def test_validate_username_existing(self):
        url = '/auth/validate-username?username=existing-user'
        response = self.client.get(url, HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Username is already in use.')

    def test_validate_username_new(self):
        url = '/auth/validate-username?username=new-user'
        response = self.client.get(url, HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'true')

    def test_register_without_activating(self):
        url = '/auth/register/'
        data = signup_data()
        response = self.client.post(url, data, format='json', HTTP_HOST=API_HOST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='test-user').exists())
        self.assertFalse(User.objects.get(username='test-user').is_active)
