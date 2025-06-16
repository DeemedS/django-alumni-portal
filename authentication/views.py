import secrets
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
import random
import string
from alumniwebsite.forms import FormWithCaptcha
from authentication.models import Course
from faculty.models import WebsiteSettings
from django.db.models import Q


User = get_user_model()

# Create your views here.
def portal(request):

    websettings = WebsiteSettings.objects.first()
    
    return render(request, 'portal.html', {
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
    })

def user_login(request):

    access_token = request.COOKIES.get('access_token')
    websettings = WebsiteSettings.objects.first()

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
            response.set_cookie('access_token', str(access_token), httponly=True, secure=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True)
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
            return render(request, 'login.html', {
                'form' : FormWithCaptcha(),
                "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
                'settings': websettings,
            })
        
    list(messages.get_messages(request))

    return render(request, 'login.html', {
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
    })

def register(request):
    courses = Course.objects.all()
    websettings = WebsiteSettings.objects.first()

    context = {
        'courses': courses,
        'form': FormWithCaptcha(),
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
    }

    if request.method == 'POST':

        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        mobile = request.POST.get('mobile')
        birthday = request.POST.get('birthday')
        sex = request.POST.get('sex')
        course = request.POST.get('course')
        course_name = request.POST.get('course_name')
        year_graduated = request.POST.get('year_graduated')
        company = request.POST.get('company')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')
        student_number = request.POST.get('student_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-pass')
        profile_image = request.FILES.get('profile_image')
        agree = request.POST.get('agree')

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

        # Validation
        if not agree:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'signup.html', context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'signup.html', context)

        if student_number and User.objects.filter(student_number=student_number).exists():
            messages.error(request, "Student number is already in use.")
            return render(request, 'signup.html', context)

        if not student_number:
            student_number = generate_student_number()

        if not course and course_name:
            course = Course.objects.filter(course_name=request.POST.get('course_name')).first()

        work_exp = [{
            "company": company,
            "position": position,
            "startDate": start_date,
            "endDate": None
        }]
        if not profile_image:
            messages.error(request, "Profile image is required.")
            return render(request, 'signup.html', context)

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
            sex=sex,
            course=Course.objects.get(id=course) if course else None,
            year_graduated=year_graduated,
            work_experience=work_exp,
            profile_image=profile_image
        )

        user.save()

        if not send_verification_email(user):
            messages.error(request, "We couldn't send the verification email.")
            return render(request, 'signup.html', context)

        if user is None:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'signup.html', context)
        
        return render(request, 'success_page.html', context)
    
    list(messages.get_messages(request))

    return render(request, 'signup.html', context)

def faculty(request):
    websettings = WebsiteSettings.objects.first()

    context = {
        'form': FormWithCaptcha(),
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
    }

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
                    return redirect('/faculty/dashboard')
                else:
                    messages.error(request, "Access denied. You are not a faculty member.")
            else:
                messages.error(request, "Your account is inactive. Contact admin for support.")
        else:
            messages.error(request, "Invalid email or password.")

    list(messages.get_messages(request))
    
    return render(request, 'faculty.html', context)


def send_verification_email(user):
    try:
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
        return True
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return False
    
def verify_email(request, uidb64, token):
    websettings = WebsiteSettings.objects.first()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        status = 404
        messages.error(request, '')
        return render(request, 'verify_email.html', {
            'status': status,
            'settings': websettings,
            "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            'form': FormWithCaptcha(),
        })
    
    if user is not None and user.email_verified:
        status = 409
        return render(request, 'verify_email.html', {
            'status': status,
            'settings': websettings,
            "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            'form': FormWithCaptcha(),
        })

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        status = 200
        return render(request, 'verify_email.html', {
            'status': status,
            'settings': websettings,
            "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            'form': FormWithCaptcha(),
        })
    else:
        status = 400
        return render(request, 'verify_email.html', {'status': status,
            'settings': websettings,
            "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            'form': FormWithCaptcha(),
        }) 

def send_password_reset_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{settings.DOMAIN_URL}/reset-password/{uid}/{token}/"

    subject = 'Reset your Alumni Portal password'
    message = f'Hi {user.email},\n\nPlease click the link below to reset your password:\n\n{reset_url}'

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False

    

def forgot_password(request):
    websettings = WebsiteSettings.objects.first()

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            messages.success(request, 'Password reset email sent.')
        except User.DoesNotExist:
            messages.error(request, 'No user with that email found.')

    return render(request, 'forgot_password.html',{
        'settings': websettings,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'form': FormWithCaptcha(),
    })

def reset_password(request, uidb64, token):
    websettings = WebsiteSettings.objects.first()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'This password reset link is invalid or has expired.')
        return render(request, 'forgot_password.html', {
            'settings': websettings,
            "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
            'form': FormWithCaptcha(),
        }) 

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-pass')

        if not new_password or not confirm_password:
            messages.error(request, 'Please fill out both password fields.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in.')
            return redirect('/login')

    return render(request, 'reset_password.html', {
        'uidb64': uidb64,
        'token': token,
        'settings': websettings,
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'form': FormWithCaptcha(),
    })

