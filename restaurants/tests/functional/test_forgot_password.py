import djoser.utils
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from restaurants.tests.functional.selenium_spec import SeleniumSpec

User = get_user_model()


class ForgotPasswordSpec(SeleniumSpec):

    def setUp(self):
        self.selenium.delete_all_cookies()
        User.objects.create_user('test-user', 'test-user@example.com', 'password')
        settings.EMAIL_SENDER.sentEmails = []

    def tearDown(self):
        User.objects.all().delete()

    def test_send_password_reset_email_to_existing_user(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/forgot"))
        email = self.selenium.find_element_by_name("email")
        email.send_keys("test-user@example.com")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('.success'))

        user = User.objects.get(username='test-user')
        uid = djoser.utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        path = "/reset/%s/%s" % (uid, token)
        self.assertEqual(len(settings.EMAIL_SENDER.sentEmails), 1)
        sent_email = settings.EMAIL_SENDER.sentEmails[0]
        self.assertEqual(sent_email.subject, 'Reset your Fud.fi password')
        self.assertIn(path, sent_email.body)
        self.assertIn('Your username is: test-user', sent_email.body)

    def test_do_not_change_password_with_invalid_uid(self):
        user = User.objects.get(username='test-user')
        token = default_token_generator.make_token(user)
        self.selenium.get('%s%s%s' % (self.live_server_url, "/reset/invalid-uid/", token))

        new_password = self.selenium.find_element_by_name("new_password")
        new_password.send_keys("new-password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('#error'))
        self.assertFalse(user.check_password('new-password'))

    def test_do_not_change_password_with_invalid_token(self):
        user = User.objects.get(username='test-user')
        uid = djoser.utils.encode_uid(user.pk)
        self.selenium.get('%s%s%s%s' % (self.live_server_url, "/reset/", uid, "/invalid-token"))

        new_password = self.selenium.find_element_by_name("new_password")
        new_password.send_keys("new-password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('#error'))
        self.assertFalse(user.check_password('new-password'))

    def test_change_password_with_valid_data(self):
        user = User.objects.get(username='test-user')
        uid = djoser.utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        self.selenium.get('%s%s%s%s%s' % (self.live_server_url, "/reset/", uid, "/", token))

        new_password = self.selenium.find_element_by_name("new_password")
        new_password.send_keys("new-password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('.success'))
        self.assertTrue(User.objects.get(username=user.username).check_password('new-password'))

    def test_reset_password_and_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/login"))
        self.selenium.find_element_by_css_selector('a.forgot-password').click()

        self.title_will_be('Forgot Password')
        email = self.selenium.find_element_by_name("email")
        email.send_keys("test-user@example.com")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(self.will_be_visible('.success'))
        self.assertEqual(len(settings.EMAIL_SENDER.sentEmails), 1)

        user = User.objects.get(username='test-user')
        uid = djoser.utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        path = "/reset/%s/%s" % (uid, token)
        self.selenium.get('%s%s' % (self.live_server_url, path))

        self.assertTrue(self.title_will_be('Reset Password'))
        new_password = self.selenium.find_element_by_name("new_password")
        new_password.send_keys("new-password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.assertTrue(self.will_be_visible('.success'))

        self.selenium.find_element_by_css_selector('.success p a').click()
        self.assertTrue(self.title_will_be('Login'))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("new-password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.title_will_be('Profile')
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))
