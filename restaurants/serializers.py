from rest_framework import serializers
from restaurants.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('name', 'subdomain', 'address', 'postal_code', 'city', 'phone_number', 'email')


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source='restaurant.subdomain', read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'title', 'content', 'restaurant', 'order')
