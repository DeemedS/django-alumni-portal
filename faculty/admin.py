from django.contrib import admin
from django.forms import ValidationError
from .models import WebsiteSettings as WebsiteSetting, Official
from django import forms

@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if WebsiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)

class OfficialAdminForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = '__all__'

    def clean_position(self):
        position = self.cleaned_data['position']
        if Official.objects.exclude(pk=self.instance.pk).filter(position=position).exists():
            raise ValidationError(f"The position '{position}' already has an official assigned.")
        return position

@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    form = OfficialAdminForm

    list_display = ('position', 'name', 'created_at')
    search_fields = ('name', 'position')
    ordering = ('position',)
    readonly_fields = ('created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # prevent changing position once saved
            return self.readonly_fields + ('position',)
        return self.readonly_fields