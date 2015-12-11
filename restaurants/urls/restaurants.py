from django.conf.urls import url
from restaurants import views

urlpatterns = [
    url(r'^$', views.restaurant_index, name='index'),
]
