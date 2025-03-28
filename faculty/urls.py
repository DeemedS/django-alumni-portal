from django.urls import path
from . import views as faculty_views
from articles import views as article_views
from users import views as user_views

app_name = 'faculty'

urlpatterns = [

    path('faculty/articles/<slug:slug>/edit', article_views.edit_article, name='edit_article'),
    path('update-order/', article_views.update_order, name='update_order'),
    
    path('faculty/dashboard', faculty_views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/logout/', faculty_views.faculty_logout, name='faculty_logout'),

    path('faculty/alumni-management', faculty_views.alumni_management, name='alumni_management'),
    path('faculty/alumni-add', user_views.alumni_add, name='alumni_add'),
    path('faculty/alumni-edit/<int:id>/', user_views.alumni_edit, name='alumni_edit'),
    path('faculty/alumni-view/<int:id>/', faculty_views.alumni_view, name='alumni_view'),
    path('faculty/alumni-delete/<int:id>/', user_views.alumni_delete, name='alumni_delete'),

    path('faculty/careers-management', faculty_views.careers_management, name='careers_management'),
    path('faculty/careers-add', faculty_views.careers_add, name='careers_add'),
    path('faculty/careers-edit/<int:id>/', faculty_views.careers_edit, name='careers_edit'),
    path('faculty/careers-view/<int:id>/', faculty_views.careers_view, name='careers_view'),
    
    path('faculty/events-management', faculty_views.events_management, name='events_management'),
    path('faculty/events-add', faculty_views.events_add, name='events_add'),
    path('faculty/events-edit/<slug:slug>/', faculty_views.events_edit, name='events_edit'),

    path('faculty/articles-management', faculty_views.articles_management, name='articles_management'),
] 