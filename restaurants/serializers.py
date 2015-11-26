from rest_framework import serializers
from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('name', 'subdomain', 'address', 'postal_code', 'city', 'phone_number', 'email')

