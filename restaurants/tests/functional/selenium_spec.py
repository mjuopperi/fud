from operator import mod

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui

from restaurants.tests.util import *


@override_settings(BASE_DOMAIN='fud.localhost')
class SeleniumSpec(StaticLiveServerTestCase):

    DEFAULT_TIMEOUT = 10

    SUBDOMAIN_INDEX = 0
    RESTAURANT_SUBDOMAINS = [
        'restaurant-0',
        'restaurant-1',
        'restaurant-2',
        'restaurant-3',
        'restaurant-4',
        'restaurant-5',
        'restaurant-6',
        'restaurant-7',
        'restaurant-8',
        'restaurant-9',
    ]

    @classmethod
    def setUpClass(cls):
        super(SeleniumSpec, cls).setUpClass()
        if in_travis():
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

    def element_exists(self, locator):
        try:
            self.selenium.find_element_by_css_selector(locator)
            return True
        except NoSuchElementException:
            return False

    def login(self):
        self.selenium.get('%s%s' % (self.server_url(), "/login"))

        username = self.selenium.find_element_by_name("username")
        username.send_keys("test-user")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("password")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.title_will_be('Profile')
        self.assertTrue(self.will_have_text('.user h2 a', 'test-user'))

    def server_url(self):
        protocol, url = self.live_server_url.split('//', 1)
        return protocol + '//fud.' + url

    def live_server_subdomain_url(self, subdomain):
        protocol, url = self.server_url().split('//', 1)
        return protocol + '//' + subdomain + '.' + url

    def create_restaurant(self, subdomain=None, user=None):
        if in_travis():
            subdomain = self.RESTAURANT_SUBDOMAINS[SeleniumSpec.SUBDOMAIN_INDEX]
            SeleniumSpec.SUBDOMAIN_INDEX = mod(SeleniumSpec.SUBDOMAIN_INDEX + 1, 10)
            return create_restaurant(subdomain, user)[0]
        else:
            return create_restaurant(subdomain, user)[0]
