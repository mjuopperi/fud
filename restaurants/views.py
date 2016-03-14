import time

from django.conf import settings
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from djoser.views import RegistrationView
from rest_framework import permissions, mixins, generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants import forms
from restaurants.models import Restaurant, Menu
from restaurants.permissions import IsOwnerOrReadOnly, RestaurantPermission
from restaurants.serializers import RestaurantSerializer, MenuSerializer


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


def activation(request):
    return render(request, 'restaurants/activation.html')


def activate(request, uid, token):
    return render(request, 'restaurants/activate.html', {
        'uid': uid,
        'token': token
    })


def profile(request):
    return render(request, 'restaurants/profile.html')


def restaurant_index(request):
    restaurant = Restaurant.objects.filter(subdomain=request.subdomain).first()
    if restaurant is not None:
        return render(request, 'restaurants/menu.html', {
            "title": restaurant.name,
            "name": restaurant.name,
        })
    else:
        raise Http404('Not found')


class CustomRegistrationView(RegistrationView):

    def send_email(self, *args, **kwargs):
        kwargs['subject_template_name'] = 'activation_email_subject.txt'
        kwargs['plain_body_template_name'] = 'activation_email_body.txt'
        settings.EMAIL_SENDER.send_email(*args, **kwargs)


class UsernameValidationView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if User.objects.filter(username=self.request.GET.get('username')).exists():
            return Response('Username is already in use.')
        else:
            return Response('true')


class SubdomainValidationView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Restaurant.objects.filter(subdomain=self.request.GET.get('subdomain')).exists():
            return Response('Subdomain is already in use.')
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


class UserRestaurantList(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class MenuList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all menus of a restaurant or create a new one
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(restaurant=Restaurant.objects.get(subdomain=self.kwargs['subdomain']))

    def get(self, request, subdomain):
        restaurant = Restaurant.objects.get(subdomain=subdomain)
        menus = Menu.objects.filter(restaurant=restaurant)
        serializer = MenuSerializer(menus, many=True)
        return Response({
            'menus': serializer.data
        })

    def post(self, request, *args, **kwargs):
        if not Restaurant.objects.filter(subdomain=kwargs['subdomain']).exists():
            raise ValidationError('Restaurant does not exist.')
        elif RestaurantPermission.has_permission(request, kwargs['subdomain']):
            return self.create(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class MenuDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Update or delete restaurants
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_object(self):
        queryset = self.get_queryset()
        restaurant = Restaurant.objects.get(subdomain=self.kwargs['subdomain'])
        filter = {'restaurant': restaurant, 'id': self.kwargs['id']}

        menu = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, restaurant)
        return menu

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if RestaurantPermission.has_permission(request, kwargs['subdomain']):
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        if RestaurantPermission.has_permission(request, kwargs['subdomain']):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class StatusCheck(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'server_time': int(time.time() * 1000)})
