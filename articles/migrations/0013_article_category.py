# Generated by Django 4.2.3 on 2024-08-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_alter_article_banner_alter_article_bodyimage_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('news', 'News'), ('Ann', 'Announcement')], default='news', max_length=10),
        ),
    ]