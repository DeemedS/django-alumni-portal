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
from django.contrib import messages
from django.contrib.messages import get_messages
import requests
from faculty.models import WebsiteSettings
from alumniwebsite.forms import FormWithCaptcha

def articles_list(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    websettings = WebsiteSettings.objects.first()

    is_authenticated = False

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
    featured_article = (
        Article.objects.filter(featured=True, is_active=True).first()
        or Article.objects.filter(is_active=True).order_by('-created_at').first()
    )

    if access_token and refresh_token:
        # Here you might want to validate the tokens or perform some action
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            is_authenticated = True


    return render(request, 'articles/articles_list.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'articles': articles,
        'school_abv': settings.SCHOOL_ABV,
        'form' : FormWithCaptcha(),
        'settings': websettings,
        'featured_article': featured_article,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'is_authenticated': is_authenticated
        
    })

def article_page(request, slug):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    websettings = WebsiteSettings.objects.first()
    
    is_authenticated = False

    article = get_object_or_404(Article, slug=slug, is_active=True)
    content_order = get_ordered_content(article)
    random_articles = Article.objects.filter(is_active=True).exclude(id=article.id).order_by('?')[:6]


    if access_token and refresh_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            is_authenticated = True

    context = {
        'article': article,
        'content_order': content_order,
        'school_abv': settings.SCHOOL_ABV,
        'form' : FormWithCaptcha(),
        'settings': websettings,
        'random_articles': random_articles,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'is_authenticated': is_authenticated
    }

    return render(request, 'articles/article_page.html', context)

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

    if request.method == 'POST': 

        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        bodytext_formset = BodyTextFormSet(request.POST, request.FILES, prefix='bodytext')
        bodyimage_formset = BodyImageFormSet(request.POST, request.FILES, prefix='bodyimage')
        subtitle_formset = SubTitleFormSet(request.POST, prefix='subtitle')

        if article_form.is_valid() and bodytext_formset.is_valid() and bodyimage_formset.is_valid() and subtitle_formset.is_valid():
            article = article_form.save()
            
            deleted_bodytext_ids = []
            deleted_bodyimage_ids = []
            deleted_subtitle_ids = []

            for form in bodytext_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_bodytext_ids.append(form.cleaned_data.get('id'))
            
            for form in bodyimage_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_bodyimage_ids.append(form.cleaned_data.get('id'))
            
            for form in subtitle_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_subtitle_ids.append(form.cleaned_data.get('id'))

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

                    if bodyimage_id in deleted_bodyimage_ids:
                        BodyImage.objects.filter(id=bodyimage_id).delete()
                        if f"bodyimage-{bodyimage_id}" in article.order:
                            article.order.remove(f"bodyimage-{bodyimage_id}")
                        article.save()

                    elif bodyimage:
                        bodyimage = get_object_or_404(BodyImage, id=bodyimage_id, article=article)
                        bodyimage.image = form.instance.image
                        bodyimage.alt = form.instance.alt
                        bodyimage.caption = form.instance.caption
                        bodyimage.date = form.instance.date
                        bodyimage.order = 'bodyimage-' + str(bodyimage_id)
                        bodyimage.save()
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
                    subtitle_id = form.cleaned_data.get('id')
                    subtitle = SubTitle.objects.filter(id=subtitle_id, article=article).first()

                    if subtitle_id in deleted_subtitle_ids:
                        SubTitle.objects.filter(id=subtitle_id).delete()
                        if f"subtitle-{subtitle_id}" in article.order:
                            article.order.remove(f"subtitle-{subtitle_id}")
                        article.save()

                    elif subtitle:
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


@login_required(login_url='/faculty/')
def toggle_article_status(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        try:
            article = Article.objects.get(id=id)
            article.is_active = not article.is_active
            article.save()
            return JsonResponse({"message": "Article status updated successfully"}, status=200)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Article not found"}, status=404)  # Not Found
        except Exception as e:
            return JsonResponse({"error": f"Error updating article status: {str(e)}"}, status=500)
    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse('authentication:faculty'))
    
@login_required(login_url='/faculty/')
def article_delete(request, id):
    career = Article.objects.filter(id=id).first()

    if not career:
        return JsonResponse({"success": False, "message": "Article not found"}, status=404)

    try:
        # Delete the article
        career.delete()
        return JsonResponse({"success": True}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "message": "Internal server error"}, status=500)
    
@login_required(login_url='/faculty/')
def article_add(request):

    BodyTextFormSet = formset_factory(BodyTextForm, extra=0)
    BodyImageFormSet = formset_factory(BodyImageForm, extra=0)
    SubTitleFormSet = formset_factory(SubTitleForm, extra=0)


    if request.method == 'POST': 
        article_form = ArticleForm(request.POST, request.FILES, instance=None)
        bodytext_formset = BodyTextFormSet(request.POST, request.FILES, prefix='bodytext')
        bodyimage_formset = BodyImageFormSet(request.POST, request.FILES, prefix='bodyimage')
        subtitle_formset = SubTitleFormSet(request.POST, prefix='subtitle')

        if article_form.is_valid() and bodytext_formset.is_valid() and bodyimage_formset.is_valid() and subtitle_formset.is_valid():
            article = article_form.save()
            
            deleted_bodytext_ids = []
            deleted_bodyimage_ids = []
            deleted_subtitle_ids = []

            for form in bodytext_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_bodytext_ids.append(form.cleaned_data.get('id'))
            
            for form in bodyimage_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_bodyimage_ids.append(form.cleaned_data.get('id'))
            
            for form in subtitle_formset:
                if form.cleaned_data.get('DELETE') == True:
                    deleted_subtitle_ids.append(form.cleaned_data.get('id'))

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

                    if bodyimage_id in deleted_bodyimage_ids:
                        BodyImage.objects.filter(id=bodyimage_id).delete()
                        if f"bodyimage-{bodyimage_id}" in article.order:
                            article.order.remove(f"bodyimage-{bodyimage_id}")
                        article.save()

                    elif bodyimage:
                        bodyimage = get_object_or_404(BodyImage, id=bodyimage_id, article=article)
                        bodyimage.image = form.instance.image
                        bodyimage.alt = form.instance.alt
                        bodyimage.caption = form.instance.caption
                        bodyimage.date = form.instance.date
                        bodyimage.order = 'bodyimage-' + str(bodyimage_id)
                        bodyimage.save()
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
                    subtitle_id = form.cleaned_data.get('id')
                    subtitle = SubTitle.objects.filter(id=subtitle_id, article=article).first()

                    if subtitle_id in deleted_subtitle_ids:
                        SubTitle.objects.filter(id=subtitle_id).delete()
                        if f"subtitle-{subtitle_id}" in article.order:
                            article.order.remove(f"subtitle-{subtitle_id}")
                        article.save()

                    elif subtitle:
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
        
            return redirect('faculty:edit_article', slug=article.slug)
        

    else:

        article_form = ArticleForm()
        bodytext_formset = BodyTextFormSet(initial=[], prefix='bodytext')
        bodyimage_formset = BodyImageFormSet(initial=[], prefix='bodyimage')
        subtitle_formset = SubTitleFormSet(initial=[], prefix='subtitle')
        
    context = {
        'article_form': article_form,
        'bodytext_formset': bodytext_formset,
        'bodyimage_formset': bodyimage_formset,
        'subtitle_formset': subtitle_formset,
        'school_abv': settings.SCHOOL_ABV
    }

    return render(request, 'faculty/add_article.html', context)