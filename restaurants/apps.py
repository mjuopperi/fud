from django.apps import AppConfig
from django.conf import settings


class RestaurantsConfig(AppConfig):
    name = 'restaurants'
    verbose_name = 'Restaurants'

    def ready(self):
        if settings.DJOSER['SEND_ACTIVATION_EMAIL']:
            from restaurants.signals.handlers import UserDisabler