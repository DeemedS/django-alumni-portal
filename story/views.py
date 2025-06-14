from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from django.conf import settings
from faculty.models import WebsiteSettings
from .models import Stories
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from alumniwebsite.forms import FormWithCaptcha
from .forms import StoriesForm
from django.contrib.auth.decorators import login_required

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
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
        'is_authenticated': is_authenticated
    }

    return render(request, 'story/story.html', context)


def story_page(request, id):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    
    story = get_object_or_404(Stories, id=id, is_active=True)
    websettings = WebsiteSettings.objects.first()

    is_authenticated = False

    if access_token and refresh_token:
        # Here you might want to validate the tokens or perform some action
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            is_authenticated = True

    context ={
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
        'is_authenticated': is_authenticated,
        'story': story

    }
    return render(request, 'story/story_page.html', context)

@login_required(login_url='/faculty/')
def story_delete(request, id):
    stories = Stories.objects.filter(id=id).first()

    if not stories:
        return JsonResponse({"success": False, "message": "Story not found"}, status=404)

    try:
        stories.delete()
        return JsonResponse({"success": True}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "message": "Internal server error"}, status=500)
    
@login_required(login_url='/faculty/')
def toggle_story_status(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        try:
            story = Stories.objects.get(id=id)
            story.is_active = not story.is_active
            story.save()
            return JsonResponse({"message": "Story status updated successfully"}, status=200)
        except Stories.DoesNotExist:
            return JsonResponse({"error": "Story not found"}, status=404)  # Not Found
        except Exception as e:
            return JsonResponse({"error": f"Error updating Story status: {str(e)}"}, status=500)
    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse('authentication:faculty'))
    
@login_required(login_url='/faculty/')
def story_add(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        return redirect(reverse('authentication:faculty'))
    # Only allow one story for non-staff users
    if not request.user.is_staff and Stories.objects.filter(user=request.user).exists():
        messages.error(request, "You have already submitted a story.")
        return redirect(reverse('faculty:story_management'))


    if request.method == 'POST':
        form = StoriesForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, "Story added successfully.")
            return redirect(reverse('faculty:story_management'))
        else:
            messages.error(request, "Error adding story. Please check the form.")
    else:
        form = StoriesForm()
    
    context = {
        'form' : form,
    }
    return render(request, 'faculty/story_add.html', context)

@login_required(login_url='/faculty/')
def story_edit(request, id):
    story = get_object_or_404(Stories, id=id)
    # Only allow editing if the story was created by a staff user
    if not story.user.is_staff:
        messages.error(request, "You are not allowed to edit alumni stories.")
        return redirect(reverse('faculty:story_management'))


    if request.method == 'POST':
        form = StoriesForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, "Story updated successfully.")
            return redirect(reverse('faculty:story_management'))
        else:
            messages.error(request, "Error updating story. Please check the form.")
    else:
        form = StoriesForm(instance=story)

    context = {
        'form': form,
        'story': story
    }
    return render(request, 'faculty/story_edit.html', context)