from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('restaurants.urls.restaurants', namespace='restaurants')),
]
