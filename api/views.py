from django.shortcuts import render
from .serializers import EventSerializer
from django.utils.timezone import now
from events.models import Event

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class FilteredEventsAPIView(APIView):
    def get(self, request, format=None):
        event_filter = request.GET.get('event_filter', 'all')
        month = request.GET.get('month', now().month)
        year = request.GET.get('year', now().year)

        events = Event.objects.all()

        if event_filter == 'past':
            events = events.filter(date__lt=now()).order_by('-date')

        elif event_filter == 'upcoming':
            events = events.filter(date__gte=now()).order_by('-date')

        else:
            events = events.order_by('-date')

        if month:
            events = events.filter(date__month=month)

        if year:
            events = events.filter(date__year=year)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)