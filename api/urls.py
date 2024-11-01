from django.urls import path
from . import views
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

    
    path('filtered-events/', views.FilteredEventsAPIView.as_view(), name='filtered_events_api'),
    path('filtered-articles/', views.FilteredArticlesAPIView.as_view(), name='filtered_articles_api'),
]