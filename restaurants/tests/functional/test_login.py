from django.contrib.auth import get_user_model

from restaurants.tests.functional.selenium_spec import SeleniumSpec

User = get_user_model()


class LoginSpec(SeleniumSpec):

    def setUp(self):
        self.selenium.delete_all_cookies()
        User.objects.create_user('test-user', 'test-user@example.com', 'password')

    def tearDown(self):
        User.objects.all().delete()

    def test_login_with_valid_credentials(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/login"))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.title_will_be('Profile'))
        self.assertTrue(self.will_have_text('.welcome', 'Hi, test-user!'))
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))

    def test_login_with_invalid_credentials(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/login"))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("incorrect")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('#error'))
        error = self.selenium.find_element_by_css_selector('#error p')
        self.assertEqual(error.text, 'Invalid username or password.')

    def test_stay_logged_in_after_reload(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/login"))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.title_will_be('Profile'))
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))

        self.selenium.refresh()
        self.assertTrue(self.title_will_be('Profile'))
        self.assertTrue(self.will_have_text('.welcome', 'Hi, test-user!'))
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))
        self.assertNotEqual(self.selenium.current_url, self.live_server_url + '/login')
