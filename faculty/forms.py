from django import forms
from .models import Official

class OfficialForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = ['position', 'name', 'photo']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }