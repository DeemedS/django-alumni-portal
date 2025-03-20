from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=120)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Section(models.Model):
    section_code = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section_code} - {self.course.course_code}"


class User(AbstractBaseUser, PermissionsMixin):
    profile_image = models.ImageField(upload_to='user/profile_pics/', default='user/profile_pics/default.jpg', blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    student_number = models.CharField(max_length=15, blank=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    suffix = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    civil_status = models.CharField(max_length=15, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    school_year = models.CharField(max_length=10, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    education = models.JSONField(default=dict, blank=True)
    licenses = models.JSONField(default=dict, blank=True)
    certifications = models.JSONField(default=dict, blank=True)
    work_experience = models.JSONField(default=dict, blank=True)
    jobs = models.JSONField(default=dict, blank=True)
    events = models.JSONField(default=dict, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def delete(self, *args, **kwargs):
        if self.profile_image and self.profile_image.name != 'user/profile_pics/default.jpg':
            if os.path.isfile(self.profile_image.path):
                os.remove(self.profile_image.path)
        super().delete(*args, **kwargs)
