from django.conf import settings
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from .forms import FormWithCaptcha
from django.core.mail import send_mail
from faculty.models import WebsiteSettings

def home(request):
    context = {'form' : FormWithCaptcha()}
    return render(request, 'home/home.html', context)

def help_email(request):

    if request.method == 'POST':
        websettings = WebsiteSettings.objects.first()

        name = request.POST.get('name')
        email = request.POST.get('emailaddress')
        year = request.POST.get('year')
        program = request.POST.get('program')
        message = request.POST.get('message')

        # Construct subject and full message
        subject = f"Assistance Request from {name} ({year}, {program})"
        full_message = f"""
        Name: {name}
        Email: {email}
        Year: {year}
        Program: {program}

        Message:
        {message}
        """

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [websettings.arcdo_email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Message sent successfully!'}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error': f'Failed to send email: {str(e)}'}, status=500)

    return HttpResponseNotAllowed(['POST'])