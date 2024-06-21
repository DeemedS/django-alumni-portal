from django.shortcuts import render

# Create your views here.

def events(request):
    return render(request, 'events/events.html')

def event_page(request, slug):
    return render(request, 'events/event_page.html')