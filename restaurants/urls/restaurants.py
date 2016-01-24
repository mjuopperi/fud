from django.conf.urls import url
from restaurants import views

app_name = 'restaurants'
urlpatterns = [
    url(r'^$', views.restaurant_index, name='index'),
]
