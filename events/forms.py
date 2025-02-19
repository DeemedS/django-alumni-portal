from django import forms
from .models import Event
from datetime import datetime
from django.utils.timezone import localtime, make_aware

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['title', 'slug', 'body', 'banner', 'thumbnail', 'date', 'time']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            local_datetime = localtime(self.instance.date)
            self.fields['date'].initial = local_datetime.date()
            self.fields['time'].initial = local_datetime.time()

    def save(self, commit=True):
        instance = super().save(commit=False)
        naive_datetime = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
        instance.date = make_aware(naive_datetime)
        if commit:
            instance.save()
        return instance