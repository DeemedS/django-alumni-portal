from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('careers/', views.careers, name='careers'),
    path('careers/<int:id>/', views.career_page, name='career_page'),
    path('careers/save_job/<int:id>/', views.save_job, name='save_job'),
    path('careers/unsave_job/<int:id>/', views.unsave_job, name='unsave_job'),
    path('careers/userjobs/', views.user_jobs, name='user_jobs'),
    path('careers/toggle_status/<int:id>/', views.toggle_status, name='toggle_status'),
]