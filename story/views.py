from django.shortcuts import render
import requests
from django.conf import settings
from faculty.models import WebsiteSettings

# Create your views here.
def story(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    websettings = WebsiteSettings.objects.first()
    is_authenticated = False

    if access_token and refresh_token:
        # Here you might want to validate the tokens or perform some action
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            is_authenticated = True

    context = {
        'settings': websettings,
        'is_authenticated': is_authenticated
    }

    return render(request, 'story/story.html', context)


def story_page(request):
    return render(request, 'story/story_page.html', {})