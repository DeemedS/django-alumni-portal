from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'student_number', 'is_staff', 'is_active',)
    list_filter = ('email', 'student_number', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'student_number', 'first_name', 'last_name', 
                        'middle_name', 'birthday', 'address', 'telephone', 'mobile', 'civil_status', 'sex', 'course', 'section', 'school_year',
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

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
