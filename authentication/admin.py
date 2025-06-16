from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section
from .models import UserSettings
from django import forms

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if current_user and not current_user.is_superuser:
            if 'is_superuser' in self.fields:
                self.fields['is_superuser'].disabled = True


class UserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm

    list_display = ('email', 'student_number', 'is_staff', 'is_active')
    list_filter = ('course', 'section', 'year_graduated', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

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

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        # Only superuser can see is_superuser field
        if request.user.is_superuser:
            for i, (name, options) in enumerate(fieldsets):
                if name == 'Permissions':
                    fields = list(options['fields'])
                    if 'is_superuser' not in fields:
                        fields.append('is_superuser')
                    fieldsets[i] = (name, {'fields': tuple(fields)})

        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        # Prevent staff from promoting anyone to superuser
        if not request.user.is_superuser:
            obj.is_superuser = False
        super().save_model(request, obj, form, change)

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_profile_image']

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSettings)

