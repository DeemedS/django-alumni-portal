from django.shortcuts import render
from .models import Article
from django.utils.timezone import now


# Create your views here.
def articles_list(request):
    current_year = now().year

    years = list(range(2010, current_year + 1))

    months = [
        {'value': 0, 'name': 'All'},
        {'value': 1, 'name': 'January'},
        {'value': 2, 'name': 'February'},
        {'value': 3, 'name': 'March'},
        {'value': 4, 'name': 'April'},
        {'value': 5, 'name': 'May'},
        {'value': 6, 'name': 'June'},
        {'value': 7, 'name': 'July'},
        {'value': 8, 'name': 'August'},
        {'value': 9, 'name': 'September'},
        {'value': 10, 'name': 'October'},
        {'value': 11, 'name': 'November'},
        {'value': 12, 'name': 'December'}
    ]

    articles = Article.objects.all().order_by('-date')

    return render(request, 'articles/articles_list.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'articles': articles
    })

def article_page(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_page.html', {'article': article})