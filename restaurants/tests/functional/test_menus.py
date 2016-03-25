from restaurants.tests.functional.selenium_spec import SeleniumSpec
from restaurants.tests.util import *

User = get_user_model()


class RestaurantMenuSpec(SeleniumSpec):

    def tearDown(self):
        Restaurant.objects.all().delete()
        Menu.objects.all().delete()
        self.clear_active_menu()

    def test_render_menus(self):
        restaurant, menu1, menu2 = self.create_restaurant_and_menus()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_be_visible('.menu-title.desktop[data-id="' + str(menu1.id) + '"]')

        active_menu_title = self.find_title_by_id(menu1.id)
        inactive_menu_title = self.find_title_by_id(menu2.id)
        self.assertEqual(active_menu_title.text, menu1.title)
        self.assertEqual(inactive_menu_title.text, menu2.title)
        self.assertIn('active', active_menu_title.get_attribute('class').split(' '))
        self.assertNotIn('active', inactive_menu_title.get_attribute('class').split(' '))

        active_menu = self.find_menu_content_by_id(menu1.id)
        inactive_menu = self.find_menu_content_by_id(menu2.id)
        self.assertTrue(active_menu.is_displayed())
        self.assertFalse(inactive_menu.is_displayed())

    def test_change_menu(self):
        restaurant, menu1, menu2 = self.create_restaurant_and_menus()
        self.selenium.get(self.live_server_subdomain_url(restaurant.subdomain))
        self.will_be_visible('.menu-title.desktop[data-id="' + str(menu1.id) + '"]')

        self.assertTrue(self.find_menu_content_by_id(menu1.id).is_displayed())
        self.assertFalse(self.find_menu_content_by_id(menu2.id).is_displayed())

        self.select_menu(menu2.id)

        self.assertFalse(self.find_menu_content_by_id(menu1.id).is_displayed())
        self.assertTrue(self.find_menu_content_by_id(menu2.id).is_displayed())
        self.assertIn('active', self.find_title_by_id(menu2.id).get_attribute('class').split(' '))

    def create_restaurant_and_menus(self):
        restaurant, _ = create_restaurant('test-restaurant')
        menu1 = create_menu(restaurant, 'Menu 1')
        menu2 = create_menu(restaurant, 'Menu 2')
        return restaurant, menu1, menu2

    def find_menu_by_id(self, menu_id):
        return self.selenium.find_element_by_css_selector('.menu[data-id="' + str(menu_id) + '"]')

    def find_menu_content_by_id(self, menu_id):
        return self.find_menu_by_id(menu_id).find_element_by_css_selector('.categories')

    def find_title_by_id(self, menu_id):
        return self.selenium.find_element_by_css_selector('.menu-title.desktop[data-id="' + str(menu_id) + '"]')

    def select_menu(self, menu_id):
        self.find_title_by_id(menu_id).click()

    def clear_active_menu(self):
        self.selenium.get('javascript:sessionStorage.clear();')
