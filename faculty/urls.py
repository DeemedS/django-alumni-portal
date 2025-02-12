from django.urls import path
from . import views as faculty_views
from articles import views as article_views

app_name = 'faculty'

urlpatterns = [

    path('faculty/articles/<slug:slug>/edit', article_views.edit_article, name='edit_article'),
    path('update-order/', article_views.update_order, name='update_order'),
    
    path('faculty/dashboard', faculty_views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/logout/', faculty_views.faculty_logout, name='faculty_logout'),
    path('faculty/alumni-management', faculty_views.alumni_management, name='alumni_management'),
    path('faculty/alumni-add', faculty_views.alumni_add, name='alumni_add'),
    path('faculty/alumni-edit', faculty_views.alumni_edit, name='alumni_edit'),
    path('faculty/alumni-view', faculty_views.alumni_view, name='alumni_view'),
    path('faculty/careers-management', faculty_views.careers_management, name='careers_management'),
    
] 