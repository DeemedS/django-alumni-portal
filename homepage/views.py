import requests
from django.shortcuts import render
from articles.models import Article
from events.models import Event
from django.conf import settings

def home(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    
    featured_article = Article.objects.filter(featured=True, is_active=True).first()
    news_articles = Article.objects.filter(featured=False, is_active=True).order_by('-date')[:2]
    event_article = Event.objects.filter(is_active=True).order_by('-date').first()

    if access_token and refresh_token:
        # Here you might want to validate the tokens or perform some action
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            context = {
                'featured_article': featured_article,
                'news_articles': news_articles,
                'event_article': event_article,
                'school_abv': settings.SCHOOL_ABV,
                'is_authenticated': True
            }

        return render(request, 'homepage/home.html', context)
    
    context = {
        'featured_article': featured_article,
        'news_articles': news_articles,
        'event_article': event_article,
        'school_abv': settings.SCHOOL_ABV,
        'is_authenticated': False
    }


    return render(request, 'homepage/home.html', context)
