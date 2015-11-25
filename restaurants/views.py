from django.shortcuts import render
from rest_framework import permissions, mixins, generics

from restaurants import forms
from restaurants.models import Restaurant
from restaurants.permissions import IsOwnerOrReadOnly
from restaurants.serializers import RestaurantSerializer


def index(request):
    return render(request, 'restaurants/index.html')


def signup(request):
    return render(request, 'restaurants/signup.html')


def login(request):
    return render(request, 'restaurants/login.html')


def register(request):
    form = forms.RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'restaurants/register.html', context)


class RestaurantList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all restaurants or create a new one
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RestaurantDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Update or delete restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'subdomain'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
