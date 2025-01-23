from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('myaccount/', views.user_dashboard , name='dashboard'),
    path('myaccount/edit/', views.user_edit, name='edit'),
    path('myaccount/logout/', views.user_logout, name='logout'),
]