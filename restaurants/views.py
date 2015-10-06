from django.shortcuts import render

from restaurants import models, forms

def index(request):
    return render(request, 'restaurants/index.html')

def signup(request):
    return render(request, 'restaurants/signup.html')

def login(request):
    return render(request, 'restaurants/login.html')

def register(request):
	form = forms.RegistrationForm()
	context = {
		'form' : form,
	}
	return render(request, 'restaurants/register.html', context)