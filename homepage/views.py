from django.shortcuts import render
from articles.models import Article
from events.models import Event
from django.conf import settings

def home(request):
    featured_article = Article.objects.filter(featured=True).first()
    news_articles = Article.objects.filter(featured=False).order_by('-date')[:2]
    event_article = Event.objects.order_by('-date').first()

    return render(request, 'homepage/home.html', {
        'featured_article': featured_article,
        'news_articles': news_articles,
        'event_article': event_article,
        'school_abv': settings.SCHOOL_ABV
    })
