from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Article
from .forms import ArticleForm
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json



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

@csrf_exempt
@require_POST
def update_order(request):
    data = json.loads(request.body)
    order = data.get('order', [])
    slug = data.get('slug')

    # Get the article and update its order
    article = Article.objects.get(slug=slug)
    article.order = order
    article.save()
    
    return JsonResponse({'status': 'success'})

def edit_article(request, slug):

    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            # Redirect back to the same page
            return redirect(reverse('faculty:edit_article', kwargs={'slug': slug}))
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
    }

    return render(request, 'faculty/edit_article.html', context)