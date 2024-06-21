from django.urls import  path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_page, name='event_page'),
]