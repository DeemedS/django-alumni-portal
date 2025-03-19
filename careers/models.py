from django.db import models

# Create your models here.
class JobPost(models.Model):
    JOB_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('IN', 'Internship'),
        ('CT', 'Contract'),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES, default='FT')
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

