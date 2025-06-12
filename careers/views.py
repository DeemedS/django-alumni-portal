import json
from django.shortcuts import get_object_or_404, render, redirect
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
from careers.models import JobPost
from faculty.models import WebsiteSettings
from alumniwebsite.forms import FormWithCaptcha

# Create your views here.

def careers(request):
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
        'settings': websettings,
        'is_authenticated': is_authenticated,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY
    }

    return render(request, 'careers/careers.html', context)


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
    job = get_object_or_404(JobPost, id=id, is_active=True)
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
        'job': job,
        'form' : FormWithCaptcha(),
        'settings': websettings,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'is_authenticated': is_authenticated
        
    }

    return render(request, 'careers/career_page.html', context)
        
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
def toggle_career_status(request, id):
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
    
@login_required(login_url='/faculty/')
def career_delete(request, id):
    career = JobPost.objects.filter(id=id).first()

    if not career:
        return JsonResponse({"success": False, "message": "Career not found"}, status=404)

    try:
        # Delete job from all users' saved jobs list
        users_with_job = User.objects.filter(jobs__contains=[{"id": id}])
        for user in users_with_job:
            user.jobs = [job for job in user.jobs if job.get("id") != id]
            user.save()

        # Delete the job post itself
        career.delete()
        return JsonResponse({"success": True}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "message": "Internal server error"}, status=500)
    
@login_required(login_url='/faculty/')
def career_add(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))
        return redirect(reverse('authentication:faculty'))

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title", "")
            company = data.get("company", "")
            company_email = data.get("company_email", "")
            company_contact = data.get("company_contact", "")
            salary = data.get("salary", "")
            location = data.get("location", "")
            job_type = data.get("job_type", "")
            description = data.get("description", "")
            responsibilities = data.get("responsibilities", "")
            qualifications = data.get("qualifications", "")
            benefits = data.get("benefits", "")

            # Save to database
            career = JobPost.objects.create(
                title=title,
                company=company,
                company_email=company_email,
                company_contact=company_contact,
                salary=salary,
                location=location,
                job_type=job_type,
                description=description,
                responsibilities=responsibilities,
                qualifications=qualifications,
                benefits=benefits,
            )
            
            career.save()

            edit_url = reverse('faculty:career_edit', args=[career.id])
            
            return JsonResponse({
                "message": "Career added successfully!",
                "redirect_url": edit_url,
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
        
    return render(request, 'faculty/careers_add.html')