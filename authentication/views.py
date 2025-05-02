import requests
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth import login


User = get_user_model()

# Create your views here.
def portal(request):
    return render(request, 'portal.html')

def user_login(request):

    access_token = request.COOKIES.get('access_token')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'User does not exist')
            return render(request, 'login.html')
        
        if not User.objects.filter(email=email, is_active=True).exists():
            messages.error(request, 'User is not active')
            return render(request, 'login.html')
        
        if not User.objects.filter(email=email, email_verified=True).exists():
            messages.error(request, 'Please verify your email address')
            return render(request, 'login.html')
            

        api_url = request.build_absolute_uri(reverse('api:token_obtain_pair'))
        response = requests.post(api_url, data={'email': email, 'password': password})
        print("API URL:", api_url)
        print("Status:", response.status_code)
        print("Response:", response.text)


        if response.status_code == 200:
            user = authenticate(request, email=email, password=password)
        else:
            messages.error(request, 'Login failed. Please check your credentials.')


        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            response = redirect('/myaccount/')
            response.set_cookie('access_token', str(access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        else:
            messages.error(request, 'Invalid email or password')


    if access_token:
        api_url = request.build_absolute_uri(reverse('api:token_verify'))
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            return redirect('/myaccount/')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-pass')
        

        # Validate form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'signup.html')

        if User.objects.filter(student_number=student_number).exists():
            messages.error(request, "Student number is already in use.")
            return render(request, 'signup.html')

        # Create the user
        user = User.objects.create_user(student_number=student_number, email=email, password=password)
        user.save()

        if user is None:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'signup.html')

        # Send verification email
        send_verification_email(user)

        return render(request, 'success_page.html')
    
    return render(request, 'signup.html')

def faculty(request):

    if request.user.is_authenticated:
        
        return redirect('/faculty/dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                if user.is_staff:
                    login(request, user)

                    context = {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                    }

                    return render(request, 'faculty_dashboard.html', context)
                else:
                    messages.error(request, "Access denied. You are not a faculty member.")
            else:
                messages.error(request, "Your account is inactive. Contact admin for support.")
        else:
            messages.error(request, "Invalid email or password.")

        return render(request, 'faculty.html')

    return render(request, 'faculty.html')


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"{settings.DOMAIN_URL}/verify-email/{uid}/{token}/"

    subject = 'Verify your Alumni Portal account'
    message = f'Hi {user.email},\n\nPlease click the link below to verify your account:\n\n{verification_url}'
    
    send_mail(
    subject,
    message,
    settings.DEFAULT_FROM_EMAIL,
    [user.email],
    fail_silently=False,
    )

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        status = 200
        return render(request, 'verify_email.html', {'status': status})
    else:
        status = 400
        return render(request, 'verify_email.html', {'status': status})


