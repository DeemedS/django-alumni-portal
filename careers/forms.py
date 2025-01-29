from django import forms
from .models import JobPost

class CareerForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__' 