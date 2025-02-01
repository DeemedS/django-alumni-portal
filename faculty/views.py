from django.shortcuts import redirect
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import logout


@login_required(login_url='/faculty/')
def faculty_dashboard(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, 'faculty_dashboard.html', context)
    

def faculty_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/faculty') 