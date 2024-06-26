from django.urls import  path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/signup/<int:id>/', views.signup_event, name='signup_event'),
    path('events/view/<slug:slug>/', views.event_page, name='event_page'),
]