# forms.py
from django import forms
from .models import Article, BodyText, BodyImage, SubTitle
from django.forms import modelformset_factory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body','slug', 'banner', 'thumbnail', 'author', 'featured', 'category']

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class BodyTextForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    DELETE = forms.BooleanField(required=False)

    class Meta:
        model = BodyText
        fields = ['id', 'bodytext', 'quoted', 'bold', 'italic', 'fontsize', 'DELETE']
        widgets = {
            'fontsize': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }

class BodyImageForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = BodyImage
        fields = ['id', 'alt', 'image', 'caption', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

BodyTextFormSet = modelformset_factory(
    BodyText, form=BodyTextForm, extra=1, can_delete=True
)

class SubTitleForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SubTitle
        fields = ['id', 'subtitle']


    
    