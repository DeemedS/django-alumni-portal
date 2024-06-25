from django.shortcuts import render
from .models import Event

# Create your views here.

def events(request):
    return render(request, 'events/events.html')

def event_page(request, slug):
    return render(request, 'events/event_page.html')