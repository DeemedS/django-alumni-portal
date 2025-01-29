from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('careers/', views.careers, name='careers'),
    path('careers/<int:id>/', views.career_page, name='career_page'),
    path('careers/save_job/<int:id>/', views.save_job, name='save_job'),
]