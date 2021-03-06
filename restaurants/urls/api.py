from django.conf.urls import url, include
from restaurants import views

app_name = 'restaurants'
urlpatterns = [
    url(r'^auth/register/$', views.CustomRegistrationView.as_view()),
    url(r'^auth/password/reset/$', views.CustomPasswordResetView.as_view()),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/validate-username/?$', views.UsernameValidationView.as_view(), name='validate-username'),
    url(r'^restaurants/?$', views.RestaurantList.as_view()),
    url(r'^restaurants/owned/?$', views.UserRestaurantList.as_view()),
    url(r'^restaurants/validate-subdomain/?$', views.SubdomainValidationView.as_view(), name='validate-subdomain'),
    url(r'^restaurants/(?P<subdomain>[\w-]+)/?$', views.RestaurantDetail.as_view()),
    url(r'^restaurants/(?P<subdomain>[\w-]+)/menus/?$', views.MenuList.as_view()),
    url(r'^restaurants/(?P<subdomain>[\w-]+)/menus/(?P<id>.+)/?$', views.MenuDetail.as_view()),
]
