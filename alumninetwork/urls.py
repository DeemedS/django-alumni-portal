from django.urls import path
from . import views

app_name = 'alumninetwork'

urlpatterns = [
    path('alumninetwork/', views.alumninetwork_home, name='alumninetwork'),

]