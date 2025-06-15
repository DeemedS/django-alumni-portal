from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('myaccount/', views.user_dashboard , name='dashboard'),
    path('myaccount/edit/', views.user_edit, name='edit'),
    path('myaccount/change-password/', views.user_change_password, name='change_password'),
    path('myaccount/saved_jobs/', views.saved_jobs, name='saved_jobs'),
    path("myaccount/saved_events/", views.saved_events, name="saved_events"),
    path('myaccount/alumni_network/', views.alumni_network, name='alumni_network'),
    path('myaccount/user_stories/', views.user_stories, name='user_stories'),
    path('myaccount/user_donation/', views.user_donation, name='user_donation'),
    path('myaccount/logout/', views.user_logout, name='logout'),

    path('myaccount/photo/upload/', views.upload_profile_photo, name='upload_profile_photo'),
    path('myaccount/photo/remove/', views.remove_profile_photo, name='remove_profile_photo'),
]