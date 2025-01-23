from django.urls import path
from . import views
from api.views import get_user_info

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


app_name = 'api'

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/user_info/', get_user_info, name='get_user_info'),

    
    path('filtered-events/', views.FilteredEventsAPIView.as_view(), name='filtered_events_api'),
    path('filtered-articles/', views.FilteredArticlesAPIView.as_view(), name='filtered_articles_api'),
    path('filtered-jobposts/', views.FilteredJobPostsAPIView.as_view(), name='filtered_jobposts_api'),
    path('job-details/<int:id>/', views.JobPostDetailView.as_view(), name='job-details'),
]