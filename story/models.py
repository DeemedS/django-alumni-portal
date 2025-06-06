from django.db import models

# Create your models here.
class stories(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    banner = models.ImageField(blank=True, null=True, upload_to='stories/banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='stories/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

