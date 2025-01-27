from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('careers/', views.careers, name='careers'),
    path('careers/<int:id>/', views.career_page, name='career_page'),
]