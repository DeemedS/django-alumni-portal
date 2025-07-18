from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section
from .models import UserSettings

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'student_number', 'is_staff', 'is_active',)
    list_filter = ('course', 'section', 'year_graduated', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'student_number', 'profile_image', 'first_name', 'last_name',
            'middle_name', 'suffix', 'birthday', 'address', 'telephone', 'mobile', 'civil_status', 'sex',
            'course', 'section', 'year_graduated', 'education', 'licenses', 'certifications', 'work_experience',
            'x_link', 'facebook_link', 'linkedin_link', 'jobs', 'events', 'email_verified'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'student_number', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        # Convert tuple to list so we can modify
        fieldsets = list(self.fieldsets)

        if request.user.is_superuser:
            # Add is_superuser to Permissions fields
            for i, (name, options) in enumerate(fieldsets):
                if name == 'Permissions':
                    fields = list(options.get('fields', ()))
                    if 'is_superuser' not in fields:
                        fields.append('is_superuser')
                    fieldsets[i] = (name, {'fields': tuple(fields)})
                    break

        return fieldsets

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_profile_image']

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSettings)

