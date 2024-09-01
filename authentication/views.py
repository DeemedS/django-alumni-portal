import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def portal(request):
    return render(request, 'portal.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        api_url = request.build_absolute_uri(reverse('api:token_obtain_pair'))
        response = requests.post(api_url, data={'username': username, 'password': password})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = redirect('/dashboard/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def faculty(request):
    return render(request, 'faculty.html')
