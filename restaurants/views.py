from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from rest_framework import permissions, mixins, generics

from restaurants import forms
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


def index(request):
    return render(request, 'restaurants/index.html')


def signup(request):
    return render(request, 'restaurants/signup.html')


def login(request):
    return render(request, 'restaurants/login.html')


def register(request):
    form = forms.RegistrationForm()
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect(reverse('restaurants:index'))
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
