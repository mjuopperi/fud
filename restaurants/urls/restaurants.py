from django.conf.urls import url
from restaurants import views

app_name = 'restaurants'
urlpatterns = [
    url(r'^$', views.RestaurantIndexView.as_view(), name='home'),
    #url(r'^menu/?$', views.restaurant_menu, name='menu'),
    url(r'^menu/?$', views.RestaurantMenuView.as_view(), name='menu'),
]
