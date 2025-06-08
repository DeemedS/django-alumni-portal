from django.urls import path
from . import views as faculty_views
from articles import views as article_views
from users import views as user_views
from careers import views as careers_views
from events import views as events_views
from story import views as stories_views

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
    path('faculty/alumni-import', faculty_views.alumni_import, name='alumni_import'),
    path('faculty/alumni-export', faculty_views.alumni_export, name='alumni_export'),
    path('user/toggle_status/<int:id>/', faculty_views.toggle_user_status, name='toggle_user_status'),

    path('faculty/careers-management', faculty_views.careers_management, name='careers_management'),
    path('faculty/career-add', careers_views.career_add, name='career_add'),
    path('faculty/careers-edit/<int:id>/', faculty_views.careers_edit, name='career_edit'),
    path('faculty/careers-view/<int:id>/', faculty_views.careers_view, name='careers_view'),
    path('faculty/career-delete/<int:id>/', careers_views.career_delete, name='career_delete'),
    
    path('faculty/events-management', faculty_views.events_management, name='events_management'),
    path('faculty/events-add', faculty_views.events_add, name='events_add'),
    path('faculty/events-view/<slug:slug>/', faculty_views.events_view, name='events_view'),
    path('faculty/events-edit/<slug:slug>/', faculty_views.events_edit, name='events_edit'),
    path('faculty/event-delete/<int:id>/', events_views.event_delete, name='event_delete'),

    path('faculty/story-management', faculty_views.story_management, name='story_management'),
    path('faculty/stories-view/<int:id>/', faculty_views.story_view, name='story_view'),
    path('faculty/stories-delete/<int:id>/', stories_views.story_delete, name='story_delete'),

    path('faculty/articles-management', faculty_views.articles_management, name='articles_management'),
    path('faculty/articles-view/<slug:slug>/', faculty_views.articles_view, name='articles_view'),
    path('faculty/article-add', article_views.article_add, name='article_add'),
    path('faculty/article-delete/<int:id>/', article_views.article_delete, name='article_delete'),

    path('faculty/system-settings', faculty_views.system_settings, name='system_settings'),
    
    path('faculty/officials-management', faculty_views.officials_management, name='officials_management'),
    path('faculty/save-officials', faculty_views.handle_officials_form, name='handle_officials_form'),
    path('faculty/save-settings', faculty_views.handle_settings_form, name='handle_settings_form'),
] 