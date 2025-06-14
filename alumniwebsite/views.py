from django.conf import settings
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render
from .forms import FormWithCaptcha
from django.core.mail import send_mail
from faculty.models import WebsiteSettings
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import json

def home(request):
    context = {'form' : FormWithCaptcha()}
    return render(request, 'home/home.html', context)

def help_email(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
        }

        verify_resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = verify_resp.json()

        if not result.get('success'):
            return JsonResponse({'error': 'Invalid reCAPTCHA. Please try again.'}, status=400)

        # Proceed if reCAPTCHA is valid
        websettings = WebsiteSettings.objects.first()

        name = request.POST.get('name')
        email = request.POST.get('emailaddress')
        year = request.POST.get('year')
        program = request.POST.get('program')
        message = request.POST.get('message')

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
            return JsonResponse({'error': f'Failed to send email: {str(e)}'}, status=500)

    return HttpResponseNotAllowed(['POST'])



def security_txt(request):
    content = """
    Contact: mailto:guianalankem@gmail.com
    Expires: 2027-12-31T23:59:00.000Z
    Preferred-Languages: en
        """.strip()
    return HttpResponse(content, content_type='text/plain')


logger = logging.getLogger(__name__)

@csrf_exempt
def csp_report_view(request):
    if request.method == "POST":
        try:
            report = json.loads(request.body.decode("utf-8"))
            logger.warning("CSP Violation: %s", json.dumps(report, indent=2))
        except Exception as e:
            logger.error("Failed to parse CSP report: %s", e)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "only POST allowed"}, status=405)

def custom_csrf_failure_view(request, reason=""):
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(f'{referer}?csrf_error=1')
    return redirect('/?csrf_error=1')