from django.urls import  path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/signup/<int:id>/', views.signup_event, name='signup_event'),
    path('events/view/<slug:slug>/', views.event_page, name='event_page'),
    path('events/save_event/<int:id>/', views.save_event, name='save_event'),
    path('events/unsave_event/<int:id>/', views.unsave_event, name='unsave_event'),
    path('events/userevents/', views.user_events, name='user_events'),
    path('events/toggle_status/<int:id>/', views.toggle_event_status, name='toggle_event_status'),
]