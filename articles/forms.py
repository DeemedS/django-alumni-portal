# forms.py
from django import forms
from .models import Article
from django.core.files.storage import default_storage

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'bodytext_2', 'bodytext_3', 'bodyimage_1', 'bodyimage_2', 
                  'slug', 'banner', 'thumbnail', 'featured']
        
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Check for file deletions and handle accordingly
        if self.instance.pk:  # Ensure this is an update
            old_instance = Article.objects.get(pk=self.instance.pk)
            
            if old_instance.bodyimage_1 and self.cleaned_data.get('bodyimage_1') != old_instance.bodyimage_1:
                self._delete_file(old_instance.bodyimage_1)
                
            if old_instance.bodyimage_2 and self.cleaned_data.get('bodyimage_2') != old_instance.bodyimage_2:
                self._delete_file(old_instance.bodyimage_2)

            if old_instance.banner and self.cleaned_data.get('banner') != old_instance.banner:
                self._delete_file(old_instance.banner)

            if old_instance.thumbnail and self.cleaned_data.get('thumbnail') != old_instance.thumbnail:
                self._delete_file(old_instance.thumbnail)

                
            order = []

            ## Update the order field
            if instance.bodytext_2:
                order.append('bodytext_2')
            if instance.bodyimage_1:
                order.append('bodyimage_1')
            if instance.bodytext_3:
                order.append('bodytext_3')
            if instance.bodyimage_2:
                order.append('bodyimage_2')


            # Delete field in order if it is empty
            if not instance.bodytext_2 and 'bodytext_2' in instance.order:
                instance.order.remove('bodytext_2')
            if not instance.bodyimage_1 and 'bodyimage_1' in instance.order:
                instance.order.remove('bodyimage_1')
            if not instance.bodytext_3 and 'bodytext_3' in instance.order:
                instance.order.remove('bodytext_3')
            if not instance.bodyimage_2 and 'bodyimage_2' in instance.order:
                instance.order.remove('bodyimage_2')
                
            instance.order = order



        if commit:
            instance.save()

        return instance

    def _delete_file(self, file_field):
        if file_field and file_field.name:
            file_path = file_field.name
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
