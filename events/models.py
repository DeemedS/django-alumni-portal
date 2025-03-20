# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField()
    banner = models.ImageField(blank=True, null=True, upload_to='events/banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='events/thumbnail/')
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
