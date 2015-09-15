from django.shortcuts import render

def index(request):
    return render(request, 'restaurants/index.html')

def register(request):
    print("register")
    return render(request, 'restaurants/register.html')

def login(request):
    print("login")
    return render(request, 'restaurants/login.html')

