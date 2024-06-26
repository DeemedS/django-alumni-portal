from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('filtered-events/', views.FilteredEventsAPIView.as_view(), name='filtered_events_api'),
]