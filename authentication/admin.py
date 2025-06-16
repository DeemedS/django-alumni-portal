from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section
from .models import UserSettings
from django import forms

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable 'is_superuser' if user is not superuser
        if not self.current_user.is_superuser:
            self.fields['is_superuser'].disabled = True

class UserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'student_number', 'is_staff', 'is_active')
    list_filter = ('course', 'section', 'year_graduated', 'is_staff', 'is_active')

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

    form = UserChangeForm  # use our custom form

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(self.fieldsets)

        # Add is_superuser to Permissions only for superusers
        if request.user.is_superuser:
            for i, (name, options) in enumerate(fieldsets):
                if name == 'Permissions':
                    fields = list(options.get('fields', ()))
                    if 'is_superuser' not in fields:
                        fields.append('is_superuser')
                    fieldsets[i] = (name, {'fields': tuple(fields)})
                    break
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Attach current user to form instance so we can disable fields dynamically
        form.current_user = request.user
        return form

    def has_add_permission(self, request):
        # Only superusers can add users (including superusers)
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Staff can change all users but cannot make themselves superuser in form
        # (Field disabling handled in form)
        return True

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_profile_image']

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSettings)

