from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('stories/', views.story, name='stories'),
    path('stories/story_page/', views.story_page, name='story_page'), #change the 'stories/story_page/' to 'stories/id/ to make it dynamic if needed
    
]