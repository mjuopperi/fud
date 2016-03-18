from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
from restaurants.tests.selenium_spec import SeleniumSpec
import djoser.utils

User = get_user_model()


class SignupSpec(SeleniumSpec):

    def setUp(self):
        User.objects.create_user('existing-user', 'existing@example.com', 'password')
        settings.EMAIL_SENDER.sentEmails = []

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_with_valid_input(self):
        self.sign_up('test-user', 'test-user@example.com', 'password')

        self.title_will_be('Account Activation')
        self.will_have_text('section h1', 'Almost done!')
        self.assertTrue(User.objects.filter(username='test-user').exists())
        self.assertEqual(len(settings.EMAIL_SENDER.sentEmails), 1)

    def test_signup_with_existing_username(self):
        self.sign_up('existing-user', 'test-user@example.com', 'password')

        self.will_be_visible('#username-error')
        self.will_have_text('#username-error', 'Username is already in use.')

    def test_signup_without_username(self):
        self.sign_up('', 'test-user@example.com', 'password')

        self.will_be_visible('#username-error')
        self.will_have_text('#username-error', 'This field is required.')

    def test_signup_without_email(self):
        self.sign_up('test-user', '', 'password')

        self.will_be_visible('#email-error')
        self.will_have_text('#email-error', 'This field is required.')

    def test_signup_with_invalid_email(self):
        self.sign_up('test-user', 'invalid', 'password')

        self.will_be_visible('#email-error')
        self.will_have_text('#email-error', 'Please enter a valid email address.')

    def test_signup_without_password(self):
        self.sign_up('test-user', 'test-user@example.com', '')

        self.will_be_visible('#password-error')
        self.will_have_text('#password-error', 'This field is required.')

    def test_signup_and_activate(self):
        self.sign_up('test-user', 'test-user@example.com', 'password')

        self.title_will_be('Account Activation')
        self.assertTrue(User.objects.filter(username='test-user').exists())

        user = User.objects.get(username='test-user')
        uid = djoser.utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        path = "/activate/%s/%s" % (uid, token)
        self.assertEqual(len(settings.EMAIL_SENDER.sentEmails), 1)
        self.assertTrue(path in settings.EMAIL_SENDER.sentEmails[0].body)

        self.selenium.get('%s%s' % (self.live_server_url, path))

        self.will_be_visible('#activate-account')
        self.selenium.find_element_by_css_selector('#activate-account').click()
        self.will_be_visible('.success')
        self.title_will_be('Login')
        self.assertTrue(User.objects.get(username='test-user').is_active)

    def sign_up(self, username, email, password):
        self.selenium.get('%s%s' % (self.live_server_url, "/signup"))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(email)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
