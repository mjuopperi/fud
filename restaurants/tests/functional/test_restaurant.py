import time

from restaurants.tests.functional.selenium_spec import SeleniumSpec
from restaurants.tests.util import *

User = get_user_model()


class RestaurantSpec(SeleniumSpec):

    def setUp(self):
        self.selenium.delete_all_cookies()

    def tearDown(self):
        User.objects.all().delete()
        Restaurant.objects.all().delete()

    def test_render_restaurant(self):
        restaurant = self.create_restaurant()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_have_text('.info h1', restaurant.name)
        self.assertFalse(self.element_exists('button.switch-mode'))

        self.assertEqual(self.selenium.find_element_by_css_selector('h3.address').text, restaurant.address)
        self.assertEqual(self.selenium.find_element_by_css_selector('h3.city').text, '%d %s' % (restaurant.postal_code, restaurant.city))
        self.assertEqual(self.selenium.find_element_by_css_selector('h3.phone').text, restaurant.phone_number)
        self.assertEqual(self.selenium.find_element_by_css_selector('h3.email').text, restaurant.email)

    def test_change_restaurant_name(self):
        user = User.objects.create_user('test-user', 'test-user@example.com', 'password')
        restaurant = self.create_restaurant(user=user)
        self.login()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_have_text('.info h1', restaurant.name)

        self.switch_mode()
        self.selenium.find_element_by_css_selector('.info button.change').click()
        name_input = self.selenium.find_element_by_css_selector('input[name="name"]')
        name_input.clear()
        name_input.send_keys('Changed')
        self.selenium.find_element_by_css_selector('.info button.save').click()

        self.assertTrue(self.will_be_visible('.info .success'))
        self.assertEqual(Restaurant.objects.get(subdomain=restaurant.subdomain).name, 'Changed')

    def test_change_restaurant_location(self):
        user = User.objects.create_user('test-user', 'test-user@example.com', 'password')
        restaurant = self.create_restaurant(user=user)
        self.login()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_have_text('.info h1', restaurant.name)

        self.switch_mode()
        self.selenium.find_element_by_css_selector('.address button.change').click()
        address_input = self.selenium.find_element_by_css_selector('input[name="address"]')
        address_input.clear()
        address_input.send_keys('M.2')

        postal_code_input = self.selenium.find_element_by_css_selector('input[name="postal_code"]')
        postal_code_input.clear()

        city_input = self.selenium.find_element_by_css_selector('input[name="city"]')
        city_input.clear()
        city_input.send_keys('Koh Mook')

        self.selenium.find_element_by_css_selector('.address button.save').click()

        self.assertTrue(self.will_be_visible('.address .success'))

        changed = Restaurant.objects.get(subdomain=restaurant.subdomain)
        self.assertEqual(changed.address, 'M.2')
        self.assertEqual(changed.postal_code, '')
        self.assertEqual(changed.city, 'Koh Mook')

    def test_change_restaurant_contact_info(self):
        user = User.objects.create_user('test-user', 'test-user@example.com', 'password')
        restaurant = self.create_restaurant(user=user)
        self.login()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_have_text('.info h1', restaurant.name)

        self.switch_mode()
        self.selenium.find_element_by_css_selector('.contact button.change').click()
        phone_number_input = self.selenium.find_element_by_css_selector('input[name="phone_number"]')
        phone_number_input.clear()
        phone_number_input.send_keys('+358 666 666')

        email_input = self.selenium.find_element_by_css_selector('input[name="email"]')
        email_input.clear()
        email_input.send_keys('changed@fud.fi')

        self.selenium.find_element_by_css_selector('.contact button.save').click()

        self.assertTrue(self.will_be_visible('.contact .success'))

        changed = Restaurant.objects.get(subdomain=restaurant.subdomain)
        self.assertEqual(changed.phone_number, '+358 666 666')
        self.assertEqual(changed.email, 'changed@fud.fi')

    def switch_mode(self):
        self.assertTrue(self.element_exists('button.switch-mode'))
        self.selenium.find_element_by_css_selector('button.switch-mode').click()
