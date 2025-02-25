# Generated by Django 4.2.3 on 2025-02-25 14:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_user_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
