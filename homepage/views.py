from django.shortcuts import render
from articles.models import Article
from events.models import Event

def home(request):
    featured_article = Article.objects.filter(featured=True).first()
    news_articles = Article.objects.filter(featured=False).order_by('-date')[:2]
    events_articles = list(Event.objects.order_by('-date')[:6])  # Convert queryset to list
    placeholders_needed = 3 - len(events_articles)

    # Add placeholder articles if needed
    for _ in range(placeholders_needed):
        events_articles.append({
            'title': 'Placeholder Title',
            'content': 'Some quick example text to build on the card title and make up the bulk of the card\'s content.',
            'banner': None
        })
        
    return render(request, 'homepage/home.html', {'featured_article': featured_article, 'news_articles': news_articles, 'events_articles': events_articles})
