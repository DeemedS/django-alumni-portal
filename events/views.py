from django.shortcuts import render
from .models import Event
from django.utils.timezone import now
from django.conf import settings


def events(request):
    current_year = now().year
    years = list(range(2010, current_year + 1))

    months = [
        {'value': 0, 'name': 'All'},
        {'value': 1, 'name': 'January'},
        {'value': 2, 'name': 'February'},
        {'value': 3, 'name': 'March'},
        {'value': 4, 'name': 'April'},
        {'value': 5, 'name': 'May'},
        {'value': 6, 'name': 'June'},
        {'value': 7, 'name': 'July'},
        {'value': 8, 'name': 'August'},
        {'value': 9, 'name': 'September'},
        {'value': 10, 'name': 'October'},
        {'value': 11, 'name': 'November'},
        {'value': 12, 'name': 'December'}
    ]
    
    return render(request, 'events/events_list.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'school_abv': settings.SCHOOL_ABV
    })

def event_page(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request, 'events/event_page.html', {'event': event, 'school_abv': settings.SCHOOL_ABV})

def signup_event(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/signup_page.html', {'event': event, 'school_abv': settings.SCHOOL_ABV})
