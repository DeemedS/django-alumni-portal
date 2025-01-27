from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('myaccount/', views.user_dashboard , name='dashboard'),
    path('myaccount/edit/', views.user_edit, name='edit'),
    path('myaccount/saved_jobs/', views.saved_jobs, name='saved_jobs'),
    path("myaccount/saved_events/", views.saved_events, name="saved_events"),
    path('myaccount/logout/', views.user_logout, name='logout'),
]