from django.db import models

# Create your models here.
class Developers(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    github_profile = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='developers/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Developers"
        ordering = ['name']