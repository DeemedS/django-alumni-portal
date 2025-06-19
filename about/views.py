from django.shortcuts import render
import requests
from django.conf import settings
from faculty.models import WebsiteSettings, POSITION_CHOICES, Official
from django.utils.text import slugify
from alumniwebsite.forms import FormWithCaptcha
# Create your views here.

def about(request):
    websettings = WebsiteSettings.objects.first()

    officials_by_position = {}

    for pos_key, _ in POSITION_CHOICES:
        slug_key = slugify(pos_key).replace('-', '_')
        official = Official.objects.filter(position=pos_key).first()
        officials_by_position[slug_key] = official

        
    context = {
        'settings': websettings,
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'officials': officials_by_position
    }

    return render(request, 'about/about.html', context)

