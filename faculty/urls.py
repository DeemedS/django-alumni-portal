from django.urls import path
from articles import views

app_name = 'faculty'

urlpatterns = [

    path('faculty/articles/<slug:slug>/edit', views.edit_article, name='edit_article'),
    path('update-order/', views.update_order, name='update_order'),
    
]