from django.conf import settings
from django.shortcuts import redirect, render
import requests
from authentication.models import Course, Section


# Create your views here.
def alumninetwork_home(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    courses = Course.objects.all()
    sections = Section.objects.all()

        
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
                "courses": courses,
                "sections": sections,
                'active_page': 'alumni_network',
                'first_name' : user_data.get('first_name'),
                'last_name' : user_data.get('last_name'),
                'profile_image': user_data.get('profile_image'),
                'is_authenticated': True,
            }
            return render(request, 'alumninetwork/alumninetwork.html',context)

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