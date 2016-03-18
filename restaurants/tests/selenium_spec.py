import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui


@override_settings(BASE_DOMAIN='localhost')
class SeleniumSpec(StaticLiveServerTestCase):

    DEFAULT_TIMEOUT = 10

    @classmethod
    def setUpClass(cls):
        super(SeleniumSpec, cls).setUpClass()
        if 'TRAVIS' in os.environ:
            cls.selenium = webdriver.Firefox()
        else:
            cls.selenium = webdriver.PhantomJS()
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumSpec, cls).tearDownClass()

    def will_be_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            ui.WebDriverWait(self.selenium, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            return True
        except TimeoutException:
            return False

    def title_will_be(self, title, timeout=DEFAULT_TIMEOUT):
        try:
            ui.WebDriverWait(self.selenium, timeout).until(EC.title_is(title))
            return True
        except TimeoutException:
            return False

    def will_have_text(self, locator, text, timeout=DEFAULT_TIMEOUT):
        try:
            ui.WebDriverWait(self.selenium, timeout).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, locator), text))
            return True
        except TimeoutException:
            return False

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/login"))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.title_will_be('Profile')
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))
