from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('filtered-events/', views.FilteredEventsAPIView.as_view(), name='filtered_events_api'),
    path('filtered-articles/', views.FilteredArticlesAPIView.as_view(), name='filtered_articles_api'),
]