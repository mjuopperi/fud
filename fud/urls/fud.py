from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^', include('restaurants.urls.fud', namespace='restaurants')),
]
