from django.contrib import admin
from .models import Stories
# Register your models here.

@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
