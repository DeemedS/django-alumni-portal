from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('portal/', views.portal , name='portal'),
    path('login/', views.login , name='login'),
    path('signup/', views.register , name='register'),
    path('faculty/', views.faculty , name='faculty')
]