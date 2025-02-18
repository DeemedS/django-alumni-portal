from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Article, BodyText, BodyImage, SubTitle
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.conf import settings
from .forms import BodyTextForm, BodyImageForm, SubTitleForm, ArticleForm
from django.forms import formset_factory
from alumniwebsite.utils.ordered_content_utils import get_ordered_content
from django.contrib.auth.decorators import login_required
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
        'articles': articles,
        'school_abv': settings.SCHOOL_ABV
    })

def article_page(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    content_order = get_ordered_content(article)

    # Render the template with the context data.
    return render(request, 'articles/article_page.html', {
        'article': article,
        'content_order': content_order,
        'school_abv': settings.SCHOOL_ABV  
    })

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

@login_required(login_url='/faculty/')
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    bodytexts = article.bodytext_set.all()
    bodyimages = article.bodyimage_set.all()
    subtitles = article.subtitle_set.all()

    BodyTextFormSet = formset_factory(BodyTextForm, extra=0)
    BodyImageFormSet = formset_factory(BodyImageForm, extra=0)
    SubTitleFormSet = formset_factory(SubTitleForm, extra=0)

    content_order = get_ordered_content(article)

    print(request.method)

    if request.method == 'POST': 

        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        bodytext_formset = BodyTextFormSet(request.POST, request.FILES, prefix='bodytext')
        bodyimage_formset = BodyImageFormSet(request.POST, request.FILES, prefix='bodyimage')
        subtitle_formset = SubTitleFormSet(request.POST, prefix='subtitle')

        if article_form.is_valid() and bodytext_formset.is_valid() and bodyimage_formset.is_valid() and subtitle_formset.is_valid():
            article = article_form.save()
            
            deleted_bodytext_ids = []

            for form in bodytext_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_bodytext_ids.append(form.cleaned_data.get('id'))

            # Handle BodyText forms
            for form in bodytext_formset:
                if form.cleaned_data:
                    bodytext_id = form.cleaned_data.get('id')
                    bodytext = BodyText.objects.filter(id=bodytext_id, article=article).first()

                    if bodytext_id in deleted_bodytext_ids:
                        BodyText.objects.filter(id=bodytext_id).delete()
                        if f"bodytext-{bodytext_id}" in article.order:
                            article.order.remove(f"bodytext-{bodytext_id}")
                        article.save()
                    elif bodytext:
                        bodytext = get_object_or_404(BodyText, id=bodytext_id, article=article)
                        bodytext.bodytext = form.instance.bodytext
                        bodytext.quoted = form.instance.quoted
                        bodytext.bold = form.instance.bold
                        bodytext.italic = form.instance.italic
                        bodytext.fontsize = form.instance.fontsize
                        bodytext.order = 'bodytext-' + str(bodytext_id)
                        bodytext.save()
                    else:
                        new_bodytext = form.save(commit=False)
                        new_bodytext.article = article
                        new_bodytext.save() 
                        new_bodytext.order = f'bodytext-{new_bodytext.id}'
                        new_bodytext.save()
                        article.order.append(new_bodytext.order)
                        article.save()
                        
            # Handle BodyImage forms
            for form in bodyimage_formset:
                if form.cleaned_data:
                    bodyimage_id = form.cleaned_data.get('id')
                    bodyimage = BodyImage.objects.filter(id=bodyimage_id, article=article).first()
                    if bodyimage:
                        bodyimage = get_object_or_404(BodyImage, id=bodyimage_id, article=article)
                        if form.instance.image:
                            bodyimage.image = form.instance.image
                        bodyimage.alt = form.instance.alt
                        bodyimage.caption = form.instance.caption
                        bodyimage.date = form.instance.date
                        bodyimage.order = 'bodyimage-' + str(bodyimage_id)
                    else:
                        new_bodyimage = form.save(commit=False)
                        new_bodyimage.article = article
                        new_bodyimage.save()
                        new_bodyimage.order = f'bodyimage-{new_bodyimage.id}'
                        new_bodyimage.save()
                        article.order.append(new_bodyimage.order)
                        article.save()

            # Handle SubTitle forms
            for form in subtitle_formset:
                if form.cleaned_data:
                    print(form.cleaned_data)
                    subtitle_id = form.cleaned_data.get('id')
                    subtitle = SubTitle.objects.filter(id=subtitle_id, article=article).first()
                    if subtitle:
                        subtitle.subtitle = form.instance.subtitle
                        subtitle.order = 'subtitle-' + str(subtitle_id)
                        subtitle.article = article
                        subtitle.save()
                    else:
                        new_subtitle = form.save(commit=False)
                        new_subtitle.article = article
                        new_subtitle.save()
                        new_subtitle.order = f'subtitle-{new_subtitle.id}'
                        new_subtitle.save()
                        article.order.append(new_subtitle.order)
                        article.save()
                else:
                    print(form.cleaned_data, 'is empty')
        
            return redirect(reverse('faculty:edit_article', kwargs={'slug': slug}))
        


    else:
        article_form = ArticleForm(instance=article)

        initial_bodytext = [{'id': bt.id, 'bodytext': bt.bodytext, 'quoted': bt.quoted, 'bold': bt.bold, 'italic': bt.italic, 'fontsize': bt.fontsize} for bt in bodytexts]
        initial_bodyimage = [{'id': bi.id, 'alt': bi.alt, 'image': bi.image, 'caption': bi.caption, 'date': bi.date} for bi in bodyimages]
        initial_subtitle = [{'id': st.id, 'subtitle': st.subtitle} for st in subtitles]

        bodytext_formset = BodyTextFormSet(initial=initial_bodytext, prefix='bodytext')
        bodyimage_formset = BodyImageFormSet(initial=initial_bodyimage, prefix='bodyimage')
        subtitle_formset = SubTitleFormSet(initial=initial_subtitle, prefix='subtitle')
        
    context = {
        'article_form': article_form,
        'article': article,
        'bodytext_formset': bodytext_formset,
        'bodyimage_formset': bodyimage_formset,
        'subtitle_formset': subtitle_formset,
        'content_order': content_order,
        'school_abv': settings.SCHOOL_ABV
    }

    return render(request, 'faculty/edit_article.html', context)