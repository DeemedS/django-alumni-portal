import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from authentication.forms import UserForm
from authentication.models import User

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

            else:   
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                email = user_data.get('email')
                student_number = user_data.get('student_number')
                
            # Now, render the dashboard template and pass the user info
            return render(request, 'user_edit.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'student_number': student_number
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