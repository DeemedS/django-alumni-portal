import requests
from django.shortcuts import render
from articles.models import Article
from events.models import Event
from faculty.models import WebsiteSettings
from django.conf import settings
from alumniwebsite.forms import FormWithCaptcha
from django.views.decorators.http import require_GET

def home(request):
    form = FormWithCaptcha()
    
    featured_article = Article.objects.filter(featured=True, is_active=True).first()
    news_articles = Article.objects.filter(featured=False, is_active=True).order_by('-date')[:2]
    event_article = Event.objects.filter(is_active=True).order_by('-date').first()
    websettings = WebsiteSettings.objects.first()

    context = {
        'featured_article': featured_article,
        'news_articles': news_articles,
        'event_article': event_article,
        'school_abv': settings.SCHOOL_ABV,
        'settings': websettings,
        "form": form,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY
    }

    return render(request, 'homepage/home.html', context)
