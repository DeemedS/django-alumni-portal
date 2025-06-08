from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('stories/', views.story, name='stories'),
    path('stories/view/<int:id>/', views.story_page, name='story_page'),
    path('stories/toggle_status/<int:id>/', views.toggle_story_status, name='toggle_story_status'),
    
]