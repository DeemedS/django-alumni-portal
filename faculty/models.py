from django.db import models
from django.core.exceptions import ValidationError

class WebsiteSettings(models.Model):
    facebook_link = models.CharField(max_length=200)
    instagram_link = models.CharField(max_length=200)
    x_link = models.CharField(max_length=200)
    linked_in_link = models.CharField(max_length=200)
    arcdo_email = models.CharField(max_length=200)
    phone_number_1 = models.CharField(max_length=200)
    phone_number_2 = models.CharField(max_length=200)
    arcdo_address = models.CharField(max_length=200)

    def clean(self):
        if WebsiteSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one WebsiteSettings instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This triggers the clean() method
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Website Setting"
        verbose_name_plural = "Website Settings"

    def __str__(self):
        return "Website Settings"
