from django.db import models
from django.conf import settings
from authentication.models import User

# Create your models here.
class Stories(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    banner = models.ImageField(blank=True, null=True, upload_to='stories/banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='stories/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Stories"
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.title

