import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

def user_dashboard(request):

    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token:
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            return render(request, 'user_dashboard.html')
        
        elif response.status_code == 401 and refresh_token:

            refresh_url = request.build_absolute_uri(reverse('api:token_refresh'))
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/dashboard/')
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')

