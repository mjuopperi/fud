from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions, mixins, generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from restaurants import forms
from restaurants.models import Restaurant
from restaurants.permissions import IsOwnerOrReadOnly
from restaurants.serializers import RestaurantSerializer

User = get_user_model()


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


class UsernameValidationView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if User.objects.filter(username=self.request.GET.get('username')).exists():
            return Response('Username is already in use.')
        else:
            return Response('true')


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
