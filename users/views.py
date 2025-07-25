import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from authentication.forms import UserForm
from authentication.models import User, Course, Section, UserSettings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
import json
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
import random
import string
from faculty.models import WebsiteSettings
from story.forms import StoriesForm
from django.contrib.auth import get_user_model
from story.models  import Stories
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.contrib.auth import update_session_auth_hash
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def user_dashboard(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if not access_token:
        return redirect('/login/')

    verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
    verify_response = requests.post(verify_url, json={'token': access_token}, headers=base_headers)

    if verify_response.status_code == 200:
        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        auth_headers = {
            **base_headers,
            'Authorization': f'Bearer {access_token}'
        }
        user_response = requests.get(user_api_url, headers=auth_headers)

        if user_response.status_code == 200:
            user_data = user_response.json()
            context = {
                'active_page': 'dashboard',
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'user_id': user_data.get('id'),
                'is_authenticated': True
            }
            return render(request, 'user_dashboard.html', context)
        else:
            return redirect('/login/')

    elif verify_response.status_code == 401 and refresh_token:
        refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
        refresh_response = requests.post(refresh_url, data={'refresh': refresh_token}, headers=base_headers)

        if refresh_response.status_code == 200:
            new_access_token = refresh_response.json().get('access')
            response = redirect('/myaccount/')
            response.set_cookie('access_token', new_access_token, httponly=True, secure=True, samesite='Lax')
            return response
        else:
            return redirect('/login/')

    else:
        return redirect('/login/')


def user_edit(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data, headers=base_headers)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        method = request.method

        if response.status_code == 200:
            user_data = user_response.json()

            alumni = get_object_or_404(User, email=user_data.get('email'))
            courses = Course.objects.all()
            sections = Section.objects.all()

            if method == 'POST':
                data = json.loads(request.body)
                try:
                    basic_info = data.get('basicInfo', {})
                    education = data.get('education', [])
                    licenses = data.get('licenses', [])
                    work_experience = data.get('workExperience', [])

                    course = basic_info.get('course')
                    
                    if not course:
                        return JsonResponse({"error": "No Course Found"}, status=404)

                    course = get_object_or_404(Course, id=course) if course else None
                    section = get_object_or_404(Section, id=basic_info.get('section')) if basic_info.get('section') else None

                    alumni.first_name = basic_info.get('firstName', alumni.first_name)
                    alumni.last_name = basic_info.get('lastName', alumni.last_name)
                    alumni.middle_name = basic_info.get('middleName', alumni.middle_name)
                    alumni.suffix = basic_info.get('suffix', alumni.suffix) 
                    alumni.email = basic_info.get('email', alumni.email)
                    alumni.address = basic_info.get('address', alumni.address)
                    alumni.birthday = parse_date(basic_info.get('birthday')) if basic_info.get('birthday') else None
                    alumni.telephone = basic_info.get('telephone', alumni.telephone)
                    alumni.mobile = basic_info.get('mobile', alumni.mobile)
                    alumni.civil_status = basic_info.get('civilStatus')
                    alumni.sex = basic_info.get('sex', alumni.sex)
                    alumni.course = course
                    alumni.section = section
                    alumni.year_graduated=basic_info.get('year_graduated', alumni.year_graduated)
                    alumni.x_link = basic_info.get('x_link', alumni.x_link)
                    alumni.facebook_link = basic_info.get('facebook_link', alumni.facebook_link)
                    alumni.linkedin_link = basic_info.get('linkedin_link', alumni.linkedin_link)
                    alumni.education = education
                    alumni.licenses = licenses
                    alumni.work_experience = work_experience

                    alumni.save()

                    return JsonResponse({"message": "Alumni updated successfully!"})
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON data"}, status=400)

            else: 
                
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                suffix = user_data.get('suffix')
                suffix = "" if suffix in (None, "None") else suffix
                email = user_data.get('email')
                student_number = user_data.get('student_number')
                middle_name = user_data.get('middle_name')
                birthday = user_data.get('birthday')
                address = user_data.get('address')
                telephone = user_data.get('telephone')
                mobile = user_data.get('mobile')
                civil_status = user_data.get('civil_status')
                sex = user_data.get('sex')
                profile_image = user_data.get('profile_image')
                work_experience = user_data.get('work_experience', [])
                education = user_data.get('education', [])
                licenses = user_data.get('licenses', [])
                course = user_data.get('course', {})
                course_display = f"{course.get('course_code', '')} - {course.get('course_name', '')}" if course else ""
                course_id = course.get('id') if course else None
                section = user_data.get('section', {})
                section_id = section.get('id') if section else None
                section_code = section.get('section_code', '') if section else ""
                year_graduated = user_data.get('year_graduated')
                facebook_link = user_data.get('facebook_link') or ""
                linkedin_link = user_data.get('linkedin_link') or ""
                x_link = user_data.get('x_link') or ""
                

            courses = Course.objects.all()
            sections = Section.objects.all()

            context = {
                "courses": courses,
                "sections": sections,
                'first_name': first_name,
                'last_name': last_name,
                'suffix': suffix,
                'email': email,
                'student_number': student_number,
                'middle_name': middle_name,
                'birthday': birthday,
                'address': address,
                'telephone': telephone,
                'mobile': mobile,
                'civil_status': civil_status,
                'sex': sex,
                'profile_image': profile_image,
                'work_experience': work_experience,
                'education': education,
                'licenses': licenses,
                'active_page': 'edit',
                'course' : course_display,
                'course_id' : course_id,
                'section_code' : section_code,
                'section_id' : section_id,
                'year_graduated' : year_graduated,
                'is_authenticated': True,
                'facebook_link' :facebook_link,
                'linkedin_link' : linkedin_link,
                'x_link' : x_link,
            }

            return render(request, 'user_edit.html', context)
        
        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')

                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
    

def user_logout(request):
    response = redirect('/login/')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def user_change_password(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if not access_token:
        return redirect('/login/')

    # Validate access token
    verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
    verify_response = requests.post(verify_url, data={'token': access_token}, headers=base_headers)

    # Try refreshing token if needed
    if verify_response.status_code == 401 and refresh_token:
        refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
        refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            access_token = new_tokens.get('access')
            response = redirect('/myaccount/')
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
            return response
        else:
            return redirect('/login/')
    elif verify_response.status_code != 200:
        return redirect('/login/')

    # Handle POST (AJAX) request to change password
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            data = json.loads(request.body)
            current_password = data.get("current_password")
            new_password = data.get("new_password")
            confirm_new_password = data.get("confirm_new_password")

            # Get user info
            user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
            user_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})

            if user_response.status_code != 200:
                return JsonResponse({'error': 'Failed to retrieve user info.'}, status=400)

            user_data = user_response.json()
            user_email = user_data.get('email')
            user = User.objects.filter(email=user_email).first()

            if not user:
                return JsonResponse({'error': 'User not found.'}, status=404)

            if not user.check_password(current_password):
                return JsonResponse({'error': 'Current password is incorrect.'}, status=400)

            if new_password != confirm_new_password:
                return JsonResponse({'error': 'New passwords do not match.'}, status=400)

            if current_password == new_password:
                return JsonResponse({'error': 'New password must be different from the current one.'}, status=400)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevent logout

            return JsonResponse({'message': 'Password changed successfully.'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Handle GET (initial page load)
    user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_response.json() if user_response.status_code == 200 else {}

    context = {
        'active_page': 'change_password',
        'first_name': user_data.get('first_name'),
        'last_name': user_data.get('last_name'),
        'profile_image': user_data.get('profile_image'),
        'is_authenticated': True,
    }

    return render(request, 'change_password.html', context)

def saved_jobs(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data, headers=base_headers)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            user_data = user_response.json()
            context = {
                'active_page': 'saved_jobs',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
            }
            return render(request, 'saved_jobs.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
    
def saved_events(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data, headers=base_headers)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            user_data = user_response.json()
            context = {
                'active_page': 'saved_events',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
            }
            return render(request, 'saved_events.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
    
@login_required(login_url='/faculty/')
def alumni_edit(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        return redirect(reverse('authentication:faculty'))
    
    alumni = get_object_or_404(User, id=id)
    courses = Course.objects.all()
    sections = Section.objects.all()

    if request.method == 'POST':
        try:

            data = json.loads(request.body)
    
            basic_info = data.get('basicInfo', {})
            education = data.get('education', [])
            licenses = data.get('licenses', [])
            work_experience = data.get('workExperience', [])

            course_name = basic_info.get('course_name')
            course = basic_info.get('course')

            def generate_course_code(course_name, max_length=10):
                acronym = ''.join(word[0] for word in course_name.split()).upper()
                return acronym[:max_length]

            if not course and course_name:
                course_code = generate_course_code(course_name)
                course = Course.objects.get_or_create(course_name=course_name, course_code=course_code)[0].id
        
            course = get_object_or_404(Course, id=course) if course else None
            section = get_object_or_404(Section, id=basic_info.get('section')) if basic_info.get('section') else None

            alumni.first_name = basic_info.get('firstName', alumni.first_name)
            alumni.last_name = basic_info.get('lastName', alumni.last_name)
            alumni.middle_name = basic_info.get('middleName', alumni.middle_name)
            alumni.suffix = basic_info.get('suffix', alumni.suffix) 
            alumni.email = basic_info.get('email', alumni.email)
            alumni.address = basic_info.get('address', alumni.address)
            alumni.birthday = parse_date(basic_info.get('birthday')) if basic_info.get('birthday') else None
            alumni.telephone = basic_info.get('telephone', alumni.telephone)
            alumni.mobile = basic_info.get('mobile', alumni.mobile)
            alumni.civil_status = basic_info.get('civilStatus')
            alumni.sex = basic_info.get('sex', alumni.sex)
            alumni.course = course
            alumni.section = section
            alumni.year_graduated=basic_info.get('year_graduated', alumni.year_graduated)
            alumni.education = education
            alumni.licenses = licenses
            alumni.work_experience = work_experience

            alumni.save()

            return JsonResponse({"message": "Alumni updated successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    context = {
        "alumni": alumni,
        "courses": courses,
        "sections": sections,
    }

    return render(request, 'faculty/alumni_edit.html', context)

@login_required(login_url='/faculty/')
def alumni_add(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")

        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            basic_info = data.get('basicInfo', {})
            education = data.get('education', [])
            licenses = data.get('licenses', [])
            work_experience = data.get('workExperience', [])

            course_name = basic_info.get('course_name')
            course = basic_info.get('course')

            def generate_course_code(course_name, max_length=10):
                acronym = ''.join(word[0] for word in course_name.split()).upper()
                return acronym[:max_length]
            
            def generate_student_number():
                while True:
                    years = [f"{i:04d}" for i in range(0, 9999)]
                    year = random.choice(years)
                    unique_number = str(random.randint(1, 99999)).zfill(5)
                    suffix = ''.join(random.choices(string.ascii_uppercase, k=2))
                    random_digits = str(random.randint(0, 9)).zfill(1)

                    student_number = f"{year}.{unique_number}.{suffix}.{random_digits}"

                    if not User.objects.filter(student_number=student_number).exists():
                        return student_number

            if not course and course_name:
                course_code = generate_course_code(course_name)
                course = Course.objects.get_or_create(course_name=course_name, course_code=course_code)[0].id
        
            course = get_object_or_404(Course, id=course) if course else None
            section = get_object_or_404(Section, id=basic_info.get('section')) if basic_info.get('section') else None

            student_number = generate_student_number()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            if User.objects.filter(email=basic_info.get('email', "")).exists():
                messages.error(request, "Email is already in use.")
                return render(request, 'signup.html')

            if User.objects.filter(student_number=student_number).exists():
                messages.error(request, "Student number is already in use.")
                return render(request, 'signup.html')

            try:
                alumni = User.objects.create(
                    first_name=basic_info.get('firstName', ""),
                    last_name=basic_info.get('lastName', ""),
                    middle_name=basic_info.get('middleName', ""),
                    suffix=basic_info.get('suffix', ""),
                    email=basic_info.get('email', ""),
                    address=basic_info.get('address', ""),
                    birthday=parse_date(basic_info.get('birthday')) if basic_info.get('birthday') else None,
                    telephone=basic_info.get('telephone', ""),
                    mobile=basic_info.get('mobile', ""),
                    civil_status=basic_info.get('civilStatus', ""),
                    sex=basic_info.get('sex', ""),
                    course=course,
                    section=section,
                    education=education,
                    licenses=licenses,
                    work_experience=work_experience,
                    student_number=student_number,
                    year_graduated=basic_info.get('year_graduated', ""),
                )

                alumni.set_password(password)

                alumni.save()
            except Exception as e:
                return JsonResponse({"error": e}, status=400)

            # Generate verification token
            token = default_token_generator.make_token(alumni)
            uid = urlsafe_base64_encode(force_bytes(alumni.pk))
            verification_url = f"{settings.DOMAIN_URL}/verify-email/{uid}/{token}/"

            # Send email with credentials and verification link
            subject = "Alumni Registration Successful - Verify Your Email"
            message = (f"Hi {alumni.email},\n\n"
                    f"Your temporary password: {password}\n\n"
                    f"Please verify your email by clicking the link below:\n"
                    f"{verification_url}")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [alumni.email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Alumni added successfully!", "alumni_id": alumni.id})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    
    courses = Course.objects.all()
    sections = Section.objects.all()

    context = {
        "courses": courses,
        "sections": sections,
    }
    return render(request, 'faculty/alumni_add.html', context)

@login_required(login_url='/faculty/')
def alumni_delete(request, id):
    if request.method == "DELETE":
        alumni = User.objects.filter(id=id).first()
        
        if not alumni:
            return JsonResponse({"success": False, "message": "Alumni not found"}, status=404)
        
        try:
            alumni.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": "Internal server error"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def user_stories(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if not access_token:
        return redirect('/login/')

    # Token verification
    verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
    verify_response = requests.post(verify_url, data={'token': access_token}, headers=base_headers)

    if verify_response.status_code != 200:
        if refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                response = redirect('/myaccount/user_stories/')
                response.set_cookie('access_token', new_access_token, httponly=True, secure=True, samesite='Lax')
                return response
        return redirect('/login/')

    # Get user info
    user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    if user_info_response.status_code != 200:
        return HttpResponseForbidden("Could not fetch user info")

    user_data = user_info_response.json()
    User = get_user_model()
    try:
        user = User.objects.get(email=user_data['email'])
    except User.DoesNotExist:
        return HttpResponseForbidden("User not found.")

    # Initialize content values
    story = None
    form = None
    stories = None

    if user.is_staff:
        # Staff: can add multiple stories
        stories = Stories.objects.filter(user=user)
        form = StoriesForm(request.POST or None, request.FILES or None)

        if request.method == 'POST' and form.is_valid():
            new_story = form.save(commit=False)
            new_story.user = user
            new_story.save()
            return redirect('users:user_stories')

    else:
        # Alumni: only one story allowed
        story = Stories.objects.filter(user=user).first()
        stories = None  # Not used for alumni

        if request.method == 'POST':
            form = StoriesForm(request.POST, request.FILES, instance=story)
            if form.is_valid():
                story_instance = form.save(commit=False)
                story_instance.user = user

                # Handle banner deletion
                if 'clear_banner' in request.POST and story and story.banner:
                    if default_storage.exists(story.banner.name):
                        default_storage.delete(story.banner.name)
                    story_instance.banner = None

                elif story and story.banner and 'banner' in request.FILES:
                    if default_storage.exists(story.banner.name):
                        default_storage.delete(story.banner.name)

                # Handle thumbnail deletion
                if 'clear_thumbnail' in request.POST and story and story.thumbnail:
                    if default_storage.exists(story.thumbnail.name):
                        default_storage.delete(story.thumbnail.name)
                    story_instance.thumbnail = None

                elif story and story.thumbnail and 'thumbnail' in request.FILES:
                    if default_storage.exists(story.thumbnail.name):
                        default_storage.delete(story.thumbnail.name)

                story_instance.save()
                return redirect('users:user_stories')
        else:
            form = StoriesForm(instance=story)
            
    context = {
        'form': form,
        'story': story,
        'stories': stories,
        'active_page': 'user_stories',
        'first_name': user_data.get('first_name'),
        'last_name': user_data.get('last_name'),
        'profile_image': user_data.get('profile_image'),
        'is_authenticated': True,
        'is_staff': user.is_staff,
    }
    return render(request, 'user_stories.html', context)

    

def user_donation(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    websettings = WebsiteSettings.objects.first()

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data, headers=base_headers)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            user_data = user_response.json()
            context = {
                'active_page': 'user_donation',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
                'settings': websettings
            }
            return render(request, 'user_donation.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')

def alumni_network(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

    base_headers = {
        'User-Agent': user_agent
    }

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data, headers=base_headers)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            user_data = user_response.json()
            context = {
                'active_page': 'alumni_network',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
            }
            return render(request, 'alumni_network.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
    
@require_POST
def remove_profile_photo(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if not access_token:
        return redirect('/login/')

    verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
    verify_response = requests.post(verify_url, data={'token': access_token})

    if verify_response.status_code == 401 and refresh_token:
        refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
        refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            access_token = new_tokens.get('access')
            response = redirect('/myaccount/')
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
            return response
        else:
            return redirect('/login/')
    elif verify_response.status_code != 200:
        return redirect('/login/')

    user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})

    if user_response.status_code != 200:
        return redirect('/login/')

    user_data = user_response.json()
    profile_image_path = user_data.get('profile_image', '')
    user_email = user_data.get('email')

    User = get_user_model()

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Normalize the profile_image_path to be relative to MEDIA_ROOT
    if profile_image_path.startswith(settings.MEDIA_URL):
        profile_image_path = profile_image_path[len(settings.MEDIA_URL):]

    # Ensure forward slashes for Linux (avoid Windows backslashes)
    profile_image_path = profile_image_path.replace('\\', '/')

    # Get default image path from UserSettings
    default_image_path = 'user/profile_pics/default.png'

    try:
        settings_obj = UserSettings.objects.first()
        if settings_obj:
            default_image_path = settings_obj.default_profile_image.name
    except UserSettings.DoesNotExist:
        pass

    if not profile_image_path or profile_image_path == default_image_path:
        return JsonResponse({'error': 'No profile photo to remove'}, status=400)

    if default_storage.exists(profile_image_path):
        default_storage.delete(profile_image_path)

    user.profile_image = default_image_path
    user.save()

    return JsonResponse({'message': 'Photo reset to default successfully'})

@require_POST
def upload_profile_photo(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if not access_token:
        return HttpResponseRedirect('/login/')

    # Verify access token
    verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
    verify_response = requests.post(verify_url, data={'token': access_token})

    if verify_response.status_code == 401 and refresh_token:
        # Refresh token
        refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
        refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            access_token = new_tokens.get('access')
            response = HttpResponseRedirect('/myaccount/')
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
            return response
        else:
            return HttpResponseRedirect('/login/')
    elif verify_response.status_code != 200:
        return HttpResponseRedirect('/login/')

    # Get user info
    user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})

    if user_response.status_code != 200:
        return HttpResponseRedirect('/login/')

    user_data = user_response.json()
    user_email = user_data.get('email')

    if not user_email:
        return JsonResponse({'error': 'User email not found'}, status=400)

    photo = request.FILES.get('photo')
    if not photo:
        return JsonResponse({'error': 'No photo uploaded'}, status=400)

    User = get_user_model()

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    extension = os.path.splitext(photo.name)[1]
    filename = f"user/profile_pics/{user.id}{extension}"

    # Delete old photo if exists
    if default_storage.exists(filename):
        default_storage.delete(filename)

    # Resize the image
    image = Image.open(photo)
    # Convert to RGB to avoid issues with PNG or other formats
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    # Resize to max 300x300 while maintaining aspect ratio
    image.thumbnail((300, 300))

    image_io = BytesIO()
    image_format = 'JPEG' if extension.lower() in ['.jpg', '.jpeg'] else 'PNG'
    image.save(image_io, format=image_format, quality=75, optimize=True)
    image_content = ContentFile(image_io.getvalue())

    # Save new photo
    path = default_storage.save(filename, image_content)
    photo_url = default_storage.url(path)

    # Update user's profile_image field
    user.profile_image.name = path
    user.save()

    return JsonResponse({'image_url': photo_url})
    