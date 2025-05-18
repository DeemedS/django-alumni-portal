from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from authentication.models import User


class Article(models.Model):
    CATEGORY_CHOICES = [('news', 'News'), ('ann', 'Announcement')]

    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    banner = models.ImageField(blank=True, null=True, upload_to='article/banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='article/thumbnails/')
    author = models.CharField(max_length=120, default='Admin')
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_articles')

    order = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='news')

    @property
    def likes_count(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.delete_files()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.featured:
            # Unset the featured flag on all other articles
            Article.objects.exclude(pk=self.pk).update(featured=False)
        
        if self.pk:
            old_article = Article.objects.filter(pk=self.pk).first()
            if old_article:
                if old_article.banner and old_article.banner != self.banner:
                    self.delete_file(old_article.banner)
                if old_article.thumbnail and old_article.thumbnail != self.thumbnail:
                    self.delete_file(old_article.thumbnail)
    
        super().save(*args, **kwargs)

    def delete_files(self):
        if self.banner:
            self.delete_file(self.banner)

        if self.thumbnail:
            self.delete_file(self.thumbnail)

    @staticmethod
    def delete_file(file_field):
        if file_field and file_field.storage.exists(file_field.path):
            file_field.storage.delete(file_field.path)

@receiver(pre_delete, sender=Article)
def delete_article_images(sender, instance, **kwargs):
    instance.delete_files()

class BodyText(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    bodytext = models.TextField()
    quoted = models.BooleanField(default=False)
    bold = models.BooleanField(default=False)
    italic = models.BooleanField(default=False)
    fontsize = models.IntegerField()
    order = models.CharField("Order Name", max_length=50, default='')

    def __str__(self):
        return self.bodytext

    def delete(self, *args, **kwargs):

        self.save()

        if self.id:
            article = self.article
            bodytext_id = str(self.order)

            if isinstance(article.order, list):
                if bodytext_id in article.order:
                    article.order.remove(bodytext_id)
                    article.save(update_fields=['order'])

        super().delete(*args, **kwargs)


class BodyImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    alt = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)

    order = models.CharField("Order Name", max_length=50, default='')

    def __str__(self):
        return self.alt

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_image = BodyImage.objects.filter(pk=self.pk).first()
            if old_image and old_image.image and old_image.image != self.image:
                self.delete_file(old_image.image)
        super().save(*args, **kwargs)

    def delete_file(self, file_field=None):
        if file_field is None:
            file_field = self.image

        if file_field and file_field.storage.exists(file_field.path):
            file_field.storage.delete(file_field.path)

@receiver(post_delete, sender=BodyImage)
def delete_image_file(sender, instance, **kwargs):
    instance.delete_file()

class SubTitle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=120)

    order = models.CharField("Order Name", max_length=50, default='')

    def __str__(self):
        return self.subtitle
    
    def delete(self, *args, **kwargs):

        self.save()

        if self.id:
            article = self.article
            subtitle_id = str(self.order)

            if isinstance(article.order, list):
                if subtitle_id in article.order:
                    article.order.remove(subtitle_id)
                    article.save(update_fields=['order'])

        super().delete(*args, **kwargs)
