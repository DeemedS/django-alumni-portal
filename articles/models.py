from django.db import models
from django.core.files.storage import default_storage

class Article(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    bodytext_2 = models.TextField(null=True, blank=True )
    bodytext_3 = models.TextField(null=True, blank=True)

    bodyimage_1 = models.ImageField(null=True, blank=True, upload_to='images/')
    bodyimage_2 = models.ImageField(null=True, blank=True, upload_to='images/')

    slug = models.SlugField()
    banner = models.ImageField(blank=True, null=True, upload_to='banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='thumbnails/')
    date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    order = models.JSONField(default=list, blank=True)
     
    def __str__(self):
        return self.title