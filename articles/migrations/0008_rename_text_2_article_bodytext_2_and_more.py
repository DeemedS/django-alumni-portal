# Generated by Django 4.2.3 on 2024-08-08 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_text_2_article_text_3_article_text_4_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='text_2',
            new_name='bodytext_2',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='text_3',
            new_name='bodytext_3',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text_4',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text_5',
        ),
    ]