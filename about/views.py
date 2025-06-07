from django.shortcuts import render
import requests
from django.conf import settings

# Create your views here.

def about(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token and refresh_token:
        # Here you might want to validate the tokens or perform some action
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            context = {
                'is_authenticated': True
            }

        return render(request, 'about/about.html', context)
    return render(request, 'about/about.html', {'is_authenticated': False})
