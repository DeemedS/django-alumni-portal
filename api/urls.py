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

    path('user_info/', get_user_info, name='get_user_info'),

    
    path('filtered-events/', views.FilteredEventsAPIView.as_view(), name='filtered_events_api'),
    path('filtered-articles/', views.FilteredArticlesAPIView.as_view(), name='filtered_articles_api'),
    path('filtered-jobposts/', views.FilteredJobPostsAPIView.as_view(), name='filtered_jobposts_api'),
    path('filtered-stories/', views.FilteredStoriesAPIView.as_view(), name='filtered_stories_api'),
    path('filtered-alumni/', views.FilteredAlumniAPIView.as_view(), name='filtered_alumni_api'),
    path('filtered-course-section/', views.FilteredCourseSectionAPIView.as_view(), name='filterd_course_section'),
    path('filtered-course-with-section/', views.FilteredCourseSectionWithOnlySectionsAPIView.as_view(), name='filterd_course_with_section'),

    path('job-details/<int:id>/', views.JobPostDetailView.as_view(), name='job-details'),
    path('event-details/<int:id>/', views.EventsDetailView.as_view(), name='event-details'),
    path("careers/userjobs/", views.UserSavedJobsView.as_view(), name="user-saved-jobs"),
    path("events/userevents/", views.UserSavedEventsView.as_view(), name="user-saved-events"),

    path('alumni-list/', views.AlumniListView.as_view(), name='alumni-list'),
    path('related-alumni/', views.RelatedAlumniListView.as_view(), name='related-alumni-list'),

    path("articles/<int:pk>/like/",  views.ToggleArticleLikeAPIView.as_view()),
    path("events/<int:pk>/like/",    views.ToggleEventLikeAPIView.as_view()),
    path("jobposts/<int:pk>/like/",  views.ToggleJobLikeAPIView.as_view())
]