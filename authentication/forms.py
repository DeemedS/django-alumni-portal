# forms.py
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'suffix', 'birthday', 'address', 'telephone', 'mobile', 'civil_status', 'sex']
