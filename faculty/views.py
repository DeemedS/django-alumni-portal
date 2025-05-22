from django.shortcuts import redirect, render, get_object_or_404
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import logout
from careers.models import JobPost
from careers.forms import CareerForm
from django.db.models import Q
from events.models import Event
from events.forms import EventForm
from django.db.models.functions import ExtractMonth
from authentication.models import User, Course, Section


@login_required(login_url='/faculty/')
def faculty_dashboard(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'dashboard',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, 'faculty_dashboard.html', context)
    

def faculty_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/faculty') 

@login_required(login_url='/faculty/')
def alumni_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))

    context = {
        'active_page':'alumni',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, 'faculty/alumni_management.html', context)

@login_required(login_url='/faculty/')
def alumni_view(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    alumni = get_object_or_404(User, id=id)

    context = {
        "alumni": alumni
    }
    return render(request, 'faculty/alumni_view.html', context)

@login_required(login_url='/faculty/')
def careers_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))
        return redirect(reverse('authentication:faculty'))

    context = {
        'active_page':'careers',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/careers_management.html', context)

@login_required(login_url='/faculty/')
def careers_edit(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    try:
        job_post = JobPost.objects.get(id=id)
    except JobPost.DoesNotExist:
        messages.error(request, "Job post not found.")
        return redirect(reverse('faculty:careers_management'))
    
    if request.method == 'POST':
        job_post.title = request.POST['title']
        job_post.company = request.POST['company']
        job_post.location = request.POST['location']
        job_post.job_type = request.POST['job_type']
        job_post.description = request.POST['description']
        job_post.responsibilities = request.POST['responsibilities']
        job_post.qualifications = request.POST['qualifications']
        job_post.benefits = request.POST['benefits']
        job_post.salary = request.POST['salary']
        job_post.is_active = 'is_active' in request.POST
        job_post.save()
        messages.success(request, "Job post updated successfully.")
        return redirect(reverse('faculty:career_edit', kwargs={'id': id}))
    
    context = {
        'job_post': job_post,
    }
    return render(request, 'faculty/careers_edit.html', context)

@login_required(login_url='/faculty/')
def careers_view(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    try:
        job_post = JobPost.objects.get(id=id)
    except JobPost.DoesNotExist:
        messages.error(request, "Job post not found.")
        return redirect(reverse('faculty:careers_management'))
    
    # Dictionary to map job type abbreviations to full labels
    job_type_labels = {
        'FT': 'Full-Time',
        'PT': 'Part-Time',
        'CT': 'Contract',
        'IN': 'Internship',
        # Add other job types here
    }
    
    # Add full job type label to job post
    job_post_with_label = {
        'id': job_post.id,
        'date_posted': job_post.created_at,
        'location': job_post.location,
        'is_active': job_post.is_active,
        'title': job_post.title,
        'company': job_post.company,
        'description': job_post.description,
        'responsibilities': job_post.responsibilities,
        'qualifications': job_post.qualifications,
        'benefits': job_post.benefits,
        'job_type_label': job_type_labels.get(job_post.job_type, job_post.job_type),
        # Add other fields as needed
    }
    
    context = {
        'job_post': job_post_with_label,
    }
    return render(request, 'faculty/careers_view.html', context)

@login_required(login_url='/faculty/')
def events_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'events',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/events_management.html', context)

@login_required(login_url='/faculty/')
def events_add(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully.")
            return redirect(reverse('faculty:events_management'))
    else:
        form = EventForm()
    
    context = {
        'form': form,
    }
    return render(request, 'faculty/events_add.html', context)

@login_required(login_url='/faculty/')
def events_edit(request, slug):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    event = get_object_or_404(Event, slug=slug)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect(reverse('faculty:events_edit', kwargs={'slug': slug}))
    else:
        form = EventForm(instance=event)
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'faculty/events_edit.html', context)

@login_required(login_url='/faculty/')
def articles_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'articles',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/articles_management.html', context)

@login_required(login_url='/faculty/')
def story_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'alumni_stories',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/story_management.html', context)