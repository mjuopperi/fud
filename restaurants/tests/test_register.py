from restaurants.tests.selenium_spec import SeleniumSpec
from .util import *

User = get_user_model()

class RegisterSpec(SeleniumSpec):

    def setUp(self):
        User.objects.create_user('test-user', 'test-user@example.com', 'password')
        self.selenium.delete_all_cookies()

    def tearDown(self):
        User.objects.all().delete()
        Restaurant.objects.all().delete()

    def test_register_with_valid_data(self):
        self.login()
        self._register({
            'name': 'Test Restaurant',
            'subdomain': 'test-restaurant',
            'address': 'Address',
            'postal_code': '12345',
            'city': 'City',
            'phone_number': '010-123456789',
            'email': 'test.restaurant@fud.fi'
        })

        self.assertTrue(self.title_will_be('Test Restaurant'))
        self.assertTrue(Restaurant.objects.filter(subdomain='test-restaurant').exists())
        restaurant = Restaurant.objects.get(subdomain='test-restaurant')
        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.address, 'Address')
        self.assertEqual(restaurant.postal_code, '12345')
        self.assertEqual(restaurant.city, 'City')
        self.assertEqual(restaurant.phone_number, '010-123456789')
        self.assertEqual(restaurant.email, 'test.restaurant@fud.fi')

    def test_register_with_invalid_data(self):
        self.login()
        self._register({
            'name': 'Test Restaurant',
            'subdomain': 'test restaurant'
        })

        self.assertTrue(self.will_be_visible('#subdomain-error'))
        subdomain_error = self.selenium.find_element_by_css_selector('#subdomain-error')
        self.assertEqual(subdomain_error.text, 'Only lower case letters, numbers and dashes are allowed.')
        self.assertFalse(Restaurant.objects.filter(subdomain='test restaurant').exists())

    def test_register_with_reserved_subdomain(self):
        self.login()
        self._register({
            'name': 'Api Restaurant',
            'subdomain': 'api'
        })

        self.assertTrue(self.will_be_visible('#subdomain-error'))
        subdomain_error = self.selenium.find_element_by_css_selector('#subdomain-error')
        self.assertEqual(subdomain_error.text, 'Subdomain is reserved.')
        self.assertFalse(Restaurant.objects.filter(subdomain='api').exists())

    def test_register_with_in_use_subdomain(self):
        create_restaurant('test-restaurant')
        self.login()
        self._register({
            'name': 'Test Restaurant',
            'subdomain': 'test-restaurant'
        })

        self.assertTrue(self.will_be_visible('#subdomain-error'))
        subdomain_error = self.selenium.find_element_by_css_selector('#subdomain-error')
        self.assertEqual(subdomain_error.text, 'Subdomain is already in use.')

    def test_register_logged_out(self):
        self._register({
            'name': 'Test Restaurant',
            'subdomain': 'test-restaurant'
        })

        self.assertTrue(self.will_be_visible('#error'))
        error = self.selenium.find_element_by_css_selector('#error')
        self.assertEqual(error.text, 'You need to be logged in to register a restaurant.')


    def _register(self, data):
        self.selenium.get('%s%s' % (self.live_server_url, "/register"))
        for name, value in data.items():
            input = self.selenium.find_element_by_name(name)
            input.send_keys(value)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
