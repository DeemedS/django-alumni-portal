from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('stories/', views.story, name='stories'),
    path('stories/view/<int:id>/', views.story_page, name='story_page'), #change the 'stories/story_page/' to 'stories/id/ to make it dynamic if needed
    
]