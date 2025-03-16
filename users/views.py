import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import get_messages
from django.urls import reverse
from authentication.forms import UserForm
from authentication.models import User, Course, Section
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.utils.dateparse import parse_date

def user_dashboard(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if access_token:
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        user_api_url = request.build_absolute_uri(reverse('api:get_user_info'))
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            user_data = user_response.json()
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')

            # Now, render the dashboard template and pass the user info
            return render(request, 'user_dashboard.html', {'first_name': first_name, 'last_name': last_name})
        
        elif response.status_code == 401 and refresh_token:
            refresh_url = request.build_absolute_uri(reverse('api:token_refresh'))
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
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        user_api_url = request.build_absolute_uri(reverse('api:get_user_info'))
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})

        method = request.method


        if response.status_code == 200:
            user_data = user_response.json()

            if method == 'POST':
                user_instance = User.objects.filter(email=user_data.get('email')).first()
                form = UserForm(request.POST, instance=user_instance)

                if form.is_valid():
                    form.save()

                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    email = user_data.get('email')
                    student_number = user_data.get('student_number')
                    middle_name = form.cleaned_data.get('middle_name')
                    birthday = form.cleaned_data.get('birthday')
                    address = form.cleaned_data.get('address')
                    telephone = form.cleaned_data.get('telephone')
                    mobile = form.cleaned_data.get('mobile')
                    civil_status = form.cleaned_data.get('civil_status')
                    sex = form.cleaned_data.get('sex')

            else: 
                
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                email = user_data.get('email')
                student_number = user_data.get('student_number')
                middle_name = user_data.get('middle_name')
                birthday = user_data.get('birthday')
                address = user_data.get('address')
                telephone = user_data.get('telephone')
                mobile = user_data.get('mobile')
                civil_status = user_data.get('civil_status')
                sex = user_data.get('sex')

            return render(request, 'user_edit.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'student_number': student_number,
                'middle_name': middle_name,
                'birthday': birthday,
                'address': address,
                'telephone': telephone,
                'mobile': mobile,
                'civil_status': civil_status,
                'sex': sex
            })
        
        elif response.status_code == 401 and refresh_token:
            refresh_url = request.build_absolute_uri(reverse('api:token_refresh'))
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
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            return render(request, 'saved_jobs.html')

        elif response.status_code == 401 and refresh_token:
            refresh_url = request.build_absolute_uri(reverse('api:token_refresh'))
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
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            # Now, render the dashboard template and pass the user info
            return render(request, 'saved_events.html')

        elif response.status_code == 401 and refresh_token:
            refresh_url = request.build_absolute_uri(reverse('api:token_refresh'))
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
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

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

            course = get_object_or_404(Course, id=basic_info.get('course')) if basic_info.get('course') else None
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