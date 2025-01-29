from django.shortcuts import render, redirect
from django.urls import reverse
from .models import JobPost
from authentication.models import User
import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def careers(request):
    return render(request, 'careers/careers.html')

def career_page(request, id):
    job = JobPost.objects.get(id=id)
    return render(request, 'careers/career_page.html', {'job': job})

def save_job(request, id):
    print("Save job request received")

    # Get access token from cookies
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized

    # Fetch user information
    user_api_url = request.build_absolute_uri(reverse('api:get_user_info'))
    try:
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
        if user_response.status_code != 200:
            return JsonResponse({"error": "Failed to authenticate user"}, status=403)  # Forbidden

        user_data = user_response.json()
        user_email = user_data.get('email')
        if not user_email:
            return JsonResponse({"error": "Invalid user data received"}, status=400)  # Bad Request

    except requests.RequestException:
        return JsonResponse({"error": "Error contacting user API"}, status=500)  # Internal Server Error

    try:
        user = User.objects.get(email=user_email)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)  # Not Found

    if id in user.jobs:
        return JsonResponse({"message": "Job already saved"}, status=200)

    user.jobs.append(id)
    try:
        user.save()
        return JsonResponse({"message": "Job saved successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error saving job: {str(e)}"}, status=500)

    