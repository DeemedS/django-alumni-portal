from django.contrib import admin
from .models import Article, BodyText, BodyImage, SubTitle
from django.core.files.storage import default_storage

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'featured')
    search_fields = ('title',)


# Register the Article model with ArticleAdmin
@admin.register(BodyText)
class BodyTextAdmin(admin.ModelAdmin):
    list_display = ('bodytext', 'quoted', 'bold', 'italic', 'fontsize', 'order')  
    search_fields = ('bodytext', 'quoted')

@admin.register(BodyImage)
class BodyImageAdmin(admin.ModelAdmin):
    list_display = ('alt', 'image', 'caption', 'order', 'date') 
    search_fields = ('alt', 'caption')

@admin.register(SubTitle)
class SubTitleAdmin(admin.ModelAdmin):
    list_display = ('subtitle', 'order') 
    search_fields = ('subtitle',)
    
admin.site.register(Article, ArticleAdmin)
