import djoser.utils
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from restaurants.tests.selenium_spec import SeleniumSpec

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
