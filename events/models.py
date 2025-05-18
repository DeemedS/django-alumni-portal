# Create your models here.
from django.db import models
from django.utils import timezone
from authentication.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField()
    banner = models.ImageField(blank=True, null=True, upload_to='events/banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='events/thumbnail/')
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_events')

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.liked_by.count()