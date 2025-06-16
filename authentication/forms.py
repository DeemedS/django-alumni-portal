# forms.py
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'suffix', 'birthday', 'address', 'telephone', 'mobile', 'civil_status', 'sex']

def has_add_permission(self, request):
    return request.user.is_superuser or request.user.is_staff

def save_model(self, request, obj, form, change):
    if not request.user.is_superuser:
        # Ensure staff cannot set is_superuser True
        obj.is_superuser = False
    super().save_model(request, obj, form, change)