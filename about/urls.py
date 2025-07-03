from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('developers/', views.developers, name='developers'),
]