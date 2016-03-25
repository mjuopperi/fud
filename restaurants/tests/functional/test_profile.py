from restaurants.tests.functional.selenium_spec import SeleniumSpec
from restaurants.tests.util import *

User = get_user_model()


class ProfileSpec(SeleniumSpec):

    def setUp(self):
        User.objects.create_user('test-user', 'test-user@example.com', 'password')

    def tearDown(self):
        User.objects.all().delete()

    def test_redirect_to_login_if_not_logged_in(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/profile"))
        self.title_will_be('Login')

    def test_change_email(self):
        self.login()
        self.selenium.find_element_by_css_selector('#change-email button.change').click()
        email_input = self.selenium.find_element_by_css_selector('input[name="email"]')
        email_input.clear()
        email_input.send_keys('changed@example.com')
        self.selenium.find_element_by_css_selector('#change-email button.save').click()

        self.assertTrue(self.will_be_visible('#change-email .success'))
        self.assertEqual(User.objects.get(username='test-user').email, 'changed@example.com')

    def test_change_password(self):
        self.login()
        self.selenium.find_element_by_css_selector('#change-password button.change').click()
        current_password = self.selenium.find_element_by_css_selector('input[name="current-password"]')
        current_password.send_keys('password')
        new_password = self.selenium.find_element_by_css_selector('input[name="new-password"]')
        new_password.send_keys('changed')
        self.selenium.find_element_by_css_selector('#change-password button.save').click()

        self.assertTrue(self.will_be_visible('#change-password .success'))
        self.assertTrue(User.objects.get(username='test-user').check_password('changed'))

    def test_render_owned_restaurants(self):
        user = User.objects.get(username='test-user')
        restaurants = [create_restaurant('first', user)[0], create_restaurant('second', user)[0]]
        self.login()
        self.will_be_visible('#restaurants li a')
        rendered = map((lambda x: x.text), self.selenium.find_elements_by_css_selector('#restaurants li a'))

        self.assertIn(restaurants[0].name, rendered)
        self.assertIn(restaurants[1].name, rendered)
