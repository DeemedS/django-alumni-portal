from django import forms
from .models import Official, WebsiteSettings

class OfficialForm(forms.ModelForm):
    remove_photo = forms.BooleanField(required=False, label="Remove current photo")
    class Meta:
        model = Official
        fields = ['position', 'name', 'photo']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('remove_photo') and instance.photo:
            instance.photo.delete(save=False)
            instance.photo = None
        if commit:
            instance.save()
        return instance
    
class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = WebsiteSettings
        fields = ['gcash_qr', 'maya_qr', 'paypal_qr']
        widgets = {
            'gcash_qr':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'maya_qr':forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'paypal_qr':forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }