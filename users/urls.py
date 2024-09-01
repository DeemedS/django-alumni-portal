from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.user_dashboard , name='dashboard'),
]