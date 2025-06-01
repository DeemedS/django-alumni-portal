import requests
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth import login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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
            

        api_url = f"{settings.API_TOKEN_URL}/token/"
        response = requests.post(api_url, data={'email': email, 'password': password})

        user = authenticate(request, email=email, password=password)

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
        api_url = f"{settings.API_TOKEN_URL}/token/verify/"
        data = {'token': access_token}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            return redirect('/myaccount/')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        mobile = request.POST.get('mobile')
        birthday = request.POST.get('birthday')
        sex = request.POST.get('sex')
        # add course, year_graduated, current position, company and etc
        student_number = request.POST.get('student_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-pass')
        agree = request.POST.get('agree')
        

        if not agree:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'signup.html')
        
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
        user = User.objects.create_user(
            student_number=student_number, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            mobile=mobile,
            birthday=birthday,
            sex = sex
            # Add other fields as necessary
            )
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

def send_password_reset_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{settings.DOMAIN_URL}/reset-password/{uid}/{token}/"

    subject = 'Reset your Alumni Portal password'
    message = f'Hi {user.email},\n\nPlease click the link below to reset your password:\n\n{reset_url}'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            return JsonResponse({'message': 'Password reset email sent.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'No user with that email found.'}, status=404)

    return render(request, 'forgot_password.html')

@csrf_exempt
def reset_password(request, uidb64, token):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_password = data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password reset successful.'})
            else:
                return JsonResponse({'error': 'Invalid or expired token.'}, status=400)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid user.'}, status=400)

    # return JsonResponse({'error': 'Invalid request method.'}, status=400)
    return render(request, 'reset_password.html')

