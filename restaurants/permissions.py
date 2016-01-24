from rest_framework import permissions

from restaurants.models import Restaurant


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class RestaurantPermission():
    """
    Custom permission to only allows owner of an restaurant to edit it's menus.
    """

    @staticmethod
    def has_permission(request, subdomain):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            restaurant = Restaurant.objects.get(subdomain=subdomain)
            return restaurant.owner == request.user
