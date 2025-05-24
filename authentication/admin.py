from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section
from .models import UserSettings

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'student_number', 'is_staff', 'is_active',)
    list_filter = ('course', 'section', 'school_year', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'student_number', 'profile_image', 'first_name', 'last_name', 
                        'middle_name', 'suffix', 'birthday', 'address', 'telephone', 'mobile', 'civil_status', 'sex', 'course', 'section', 'school_year',
                        'education', 'licenses', 'certifications', 'work_experience',
                        'jobs', 'events', 
                        'email_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','student_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_profile_image']

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSettings)

