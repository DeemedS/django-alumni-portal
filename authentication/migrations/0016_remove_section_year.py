# Generated by Django 4.2.3 on 2025-03-11 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_section_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='year',
        ),
    ]
