from django.shortcuts import render

def index(request):
    return render(request, 'restaurants/index.html')

def signup(request):
    return render(request, 'restaurants/signup.html')

def login(request):
    return render(request, 'restaurants/login.html')

