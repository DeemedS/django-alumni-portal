from django.db import models
from django.utils import timezone

class Article(models.Model):

    category_choices = [ ('news', 'News'), ('Ann', 'Announcement')]

    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField()
    banner = models.ImageField(blank=True, null=True, upload_to='banners/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='thumbnails/')
    author = models.CharField(max_length=120, default='Admin')
    date = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)

    order = models.JSONField(default=list, blank=True)
    
    category = models.CharField(max_length=10, choices=category_choices, default='news')
     
    def __str__(self):
        return self.title

class BodyText(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    bodytext = models.TextField()
    quoted = models.BooleanField(default=False)
    bold = models.BooleanField(default=False)
    italic = models.BooleanField(default=False)
    fontsize = models.IntegerField()

    order = models.CharField(("Order Name"), max_length=50, default='')

    def __str__(self):
        return self.bodytext
    
class BodyImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    alt = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)

    order = models.CharField(("Order Name"), max_length=50, default='')

    def __str__(self):
        return self.alt
    
class SubTitle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=120)

    order = models.CharField(("Order Name"), max_length=50, default='')

    def __str__(self):
        return self.subtitle