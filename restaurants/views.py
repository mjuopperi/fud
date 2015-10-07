from django.shortcuts import render

from restaurants import models, forms

def index(request):
    return render(request, 'restaurants/index.html')

def signup(request):
    return render(request, 'restaurants/signup.html')

def login(request):
    return render(request, 'restaurants/login.html')

def register(request):
	if request.method == 'POST':
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			restaurant = form.save(commit=False)
			restaurant.owner = request.user
			restaurant.save()
	form = forms.RegistrationForm()
	context = {
		'form' : form,
		'user' : request.user,
	}
	return render(request, 'restaurants/register.html', context)