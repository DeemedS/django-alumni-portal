import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from authentication.forms import UserForm
from authentication.models import User, Course, Section
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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


def user_dashboard(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            user_data = user_response.json()
            context = {
                'active_page': 'dashboard',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True
            }

            # Now, render the dashboard template and pass the user info
            return render(request, 'user_dashboard.html', context)
        
        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')


def user_edit(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        method = request.method


        if response.status_code == 200:
            user_data = user_response.json()

            if method == 'POST':
                user_instance = User.objects.filter(email=user_data.get('email')).first()
                form = UserForm(request.POST, instance=user_instance)

                if form.is_valid():

                    print(form.cleaned_data)

                    form.save()

                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    suffix = form.cleaned_data.get('suffix')
                    suffix = "" if suffix in (None, "None") else suffix
                    email = user_data.get('email')
                    student_number = user_data.get('student_number')
                    middle_name = form.cleaned_data.get('middle_name')
                    birthday = form.cleaned_data.get('birthday')
                    address = form.cleaned_data.get('address')
                    telephone = form.cleaned_data.get('telephone')
                    mobile = form.cleaned_data.get('mobile')
                    civil_status = form.cleaned_data.get('civil_status')
                    sex = form.cleaned_data.get('sex')
                    profile_image = form.cleaned_data.get('profile_image')
                    work_experience = user_data.get('work_experience', [])
                    education = user_data.get('education', [])
                    licenses = user_data.get('licenses', [])


                    return redirect('/myaccount/edit/')

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
                school_year = user_data.get('school_year')
                

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
                'school_year' : school_year,
                'is_authenticated': True,
            }

            return render(request, 'user_edit.html', context)
        
        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True)

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

def saved_jobs(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

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
                response.set_cookie('access_token', access_token, httponly=True)
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


    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

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
                response.set_cookie('access_token', access_token, httponly=True)
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

                    student_number = f"{year}-{unique_number}-{suffix}-{random_digits}"

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
                work_experience=work_experience
            )

            alumni.set_password(password)

            alumni.save()

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

            return JsonResponse({"message": "Alumni added successfully!"})
        
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

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            user_data = user_response.json()
            context = {
                'active_page': 'user_stories',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
            }
            return render(request, 'user_stories.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')

def user_donation(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

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
            }
            return render(request, 'user_donation.html',context)

        elif response.status_code == 401 and refresh_token:
            refresh_url = f"{settings.API_TOKEN_URL}/token/refresh/"
            refresh_response = requests.post(refresh_url, data={'refresh': refresh_token})

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                access_token = new_tokens.get('access')
                response = redirect('/myaccount/')
                response.set_cookie('access_token', access_token, httponly=True)
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

    if access_token:
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

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
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')