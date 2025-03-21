# Generated by Django 4.2.3 on 2025-03-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='article/banners/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='article/thumbnails/'),
        ),
    ]
