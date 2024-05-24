from django.shortcuts import render
from .models import Article


# Create your views here.
def articles_list(request):
    articles = Article.objects.all().order_by('-date')
    return render(request, 'articles/articles_list.html', {'articles': articles})

def article_page(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_page.html', {'article': article})