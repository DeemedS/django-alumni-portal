from django.contrib import admin
from .models import Article
from django.core.files.storage import default_storage

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'featured')
    search_fields = ('title',)

    def delete_model(self, request, obj):
        # Delete associated files if they exist
        self._delete_file(obj.bodyimage_1)
        self._delete_file(obj.bodyimage_2)
        self._delete_file(obj.banner)
        self._delete_file(obj.thumbnail)
        
        super().delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        if change:
            # Handle file changes when updating
            old_instance = Article.objects.get(pk=obj.pk)
            
            # Remove files from the file system if they are cleared or replaced
            self._check_file_change(old_instance.bodyimage_1, obj.bodyimage_1)
            self._check_file_change(old_instance.bodyimage_2, obj.bodyimage_2)
            self._check_file_change(old_instance.banner, obj.banner)
            self._check_file_change(old_instance.thumbnail, obj.thumbnail)

        # Update the order field
        order = []
        if obj.bodytext_2:
            order.append('bodytext_2')
        if obj.bodyimage_1:
            order.append('bodyimage_1')
        if obj.bodytext_3:
            order.append('bodytext_3')
        if obj.bodyimage_2:
            order.append('bodyimage_2')
        obj.order = order
        obj.save()
        
        super().save_model(request, obj, form, change)

    def _check_file_change(self, old_file, new_file):
        if old_file and new_file and old_file != new_file:
            self._delete_file(old_file)
        elif old_file and not new_file:
            self._delete_file(old_file)

    def _delete_file(self, file_field):
        if file_field and file_field.name:
            file_path = file_field.name
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

# Register the Article model with ArticleAdmin
admin.site.register(Article, ArticleAdmin)
