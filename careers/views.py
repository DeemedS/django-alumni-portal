from django.shortcuts import render, redirect
from django.urls import reverse
from .models import JobPost
from authentication.models import User
import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages

# Create your views here.

def careers(request):
    return render(request, 'careers/careers.html')

def user_jobs(request):
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        return JsonResponse({"jobs": []})  # Return an empty array if unauthorized

    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
    
    if user_response.status_code != 200:
        return JsonResponse({"jobs": []})  # Return an empty array if request fails

    user_data = user_response.json()
    userjobs = user_data.get('jobs', [])  # Ensure it's an array

    return JsonResponse({"jobs": userjobs})

def career_page(request, id):
    job = JobPost.objects.get(id=id)
    return render(request, 'careers/career_page.html', {'job': job})

def save_job(request, id):

    # Get access token from cookies
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized

    # Fetch user information
    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
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

    if any(job["id"] == id for job in user.jobs):
        return JsonResponse({"message": "Job already saved"}, status=200)

    user.jobs.append({"id": id, "saved_at": now().isoformat()})

    try:
        user.save()
        return JsonResponse({"message": "Job saved successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error saving job: {str(e)}"}, status=500)

def unsave_job(request, id):

    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized


    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
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

    if not isinstance(user.jobs, list):
        return JsonResponse({"error": "Invalid data format for jobs"}, status=400)  # Bad Request

    try:
        # Extract job IDs from user.jobs list
        job_ids = [job["id"] for job in user.jobs if isinstance(job, dict)]

        if id in job_ids:
            # Remove the job dictionary where "id" matches
            user.jobs = [job for job in user.jobs if job["id"] != id]
            user.save(update_fields=['jobs'])
            return JsonResponse({"message": "Job removed successfully"}, status=200)
        else:
            return JsonResponse({"error": "Job not found in saved jobs"}, status=404)  # Not Found

    except Exception as e:
        return JsonResponse({"error": f"Error removing job: {str(e)}"}, status=500)
    

@login_required(login_url='/faculty/')
def toggle_status(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        try:
            job = JobPost.objects.get(id=id)
            job.is_active = not job.is_active
            job.save()
            return JsonResponse({"message": "Job status updated successfully"}, status=200)
        except JobPost.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)  # Not Found
        except Exception as e:
            return JsonResponse({"error": f"Error updating job status: {str(e)}"}, status=500)
    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse('authentication:faculty'))