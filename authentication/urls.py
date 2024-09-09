from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('portal/', views.portal , name='portal'),
    path('login/', views.login , name='login'),
    path('signup/', views.register , name='register'),
    path('faculty/', views.faculty , name='faculty'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify-email'),
]