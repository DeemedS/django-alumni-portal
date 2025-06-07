from django.db import models
from django.core.exceptions import ValidationError

class WebsiteSettings(models.Model):
    facebook_link = models.CharField(max_length=200, blank=True)
    instagram_link = models.CharField(max_length=200, blank=True)
    x_link = models.CharField(max_length=200, blank=True)
    linked_in_link = models.CharField(max_length=200, blank=True)
    arcdo_email = models.CharField(max_length=200, blank=True)
    phone_number_1 = models.CharField(max_length=200, blank=True)
    phone_number_2 = models.CharField(max_length=200, blank=True)
    phone_number_3 = models.CharField(max_length=200, blank=True)
    arcdo_address_line1 = models.CharField(max_length=200, blank=True)
    arcdo_address_line2 = models.CharField(max_length=200, blank=True)
    arcdo_address_line3 = models.CharField(max_length=200, blank=True)

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

POSITION_CHOICES = [
    # ARCDO OFFICIALS
    ('Director', 'Director'),
    ('Chief, Career Development & Placement Services', 'Chief, Career Development & Placement Services'),
    ('Chief, Alumni Relations Services', 'Chief, Alumni Relations Services'),
    ('Admin Staff 1', 'Admin Staff 1'),
    ('Admin Staff 2', 'Admin Staff 2'),
    ('Admin Staff 3', 'Admin Staff 3'),
    ('Admin Staff 4', 'Admin Staff 4'),

    # EXECUTIVE OFFICIALS
    ('President', 'President'),
    ('Executive Vice President', 'Executive Vice President'),
    ('Vice President for Academic Affairs', 'Vice President for Academic Affairs'),
    ('Vice President for Student Affairs & Services', 'Vice President for Student Affairs & Services'),
    ('Vice President for Research, Extension, & Dev\'t', 'Vice President for Research, Extension, & Dev\'t'),
    ('Vice President for Branches & Campuses', 'Vice President for Branches & Campuses'),
    ('Vice President for Administration', 'Vice President for Administration'),
    ('Vice President for Finance', 'Vice President for Finance'),
]

class Official(models.Model):
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='officials_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position} - {self.name}"

