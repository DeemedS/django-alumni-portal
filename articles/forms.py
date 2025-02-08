# forms.py
from django import forms
from .models import Article, BodyText, BodyImage, SubTitle
from django.forms import modelformset_factory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','slug',  'category', 'author',  'body' , 'banner', 'thumbnail', 'featured',]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class BodyTextForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    DELETE = forms.BooleanField(required=False)
    fontsize = forms.IntegerField(
        initial=15,  # Set default value
        widget=forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'form-control mb-3'})
    )

    class Meta:
        model = BodyText
        fields = ['id', 'bodytext', 'quoted', 'bold', 'italic', 'fontsize', 'DELETE']
        widgets = {
            'bodytext': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'quoted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bold': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'italic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BodyImageForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = BodyImage
        fields = ['id', 'alt', 'image', 'caption', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'alt': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
            'caption': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }

BodyTextFormSet = modelformset_factory(
    BodyText, form=BodyTextForm, extra=1, can_delete=True
)

class SubTitleForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SubTitle
        fields = ['id', 'subtitle']
        widgets = {
            'subtitle': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }


    
    