from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from restaurants import models, forms

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
		'form' : form,
	}
	return render(request, 'restaurants/register.html', context)