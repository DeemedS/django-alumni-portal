from django import forms
from .models import Stories

class StoriesForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title', 'body', 'banner', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }