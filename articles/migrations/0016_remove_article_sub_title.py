# Generated by Django 4.2.3 on 2024-08-09 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_remove_article_bodyimage_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='sub_title',
        ),
    ]
