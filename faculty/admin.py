from django.contrib import admin
from .models import WebsiteSettings as WebsiteSetting

@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if WebsiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)
