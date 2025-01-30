from django.shortcuts import render, redirect
from .models import Event
from authentication.models import User
import requests
from django.utils.timezone import now
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

def events(request):
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
    
    return render(request, 'events/events_list.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
    })

def event_page(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request, 'events/event_page.html', {'event': event})

def signup_event(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/signup_page.html', {'event': event})

def save_event(request, id):

    # Get access token from cookies
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized
    
    # fetch user informations

    user_api_url = request.build_absolute_uri(reverse('api:get_user_info'))
    try:
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
        if user_response.status_code != 200:
            return JsonResponse({"error": "Failed to authenticate user"}, status=403) 
        
        user_data = user_response.json()
        user_email = user_data.get('email')
        if not user_email:
            return JsonResponse({"error": "Invalid user data received"}, status=400)
    
    except requests.RequestException:
        return JsonResponse({"error": "Error contacting user API"}, status=500)
    
    try:
        user = User.objects.get(email=user_email)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    if id in user.events:
        return JsonResponse({"message": "Event already saved"}, status=200)
    
    user.events.append(id)
    try:
        user.save()
        return JsonResponse({"message": "Event saved successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error saving event: {str(e)}"}, status=500)

