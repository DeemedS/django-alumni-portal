# Generated by Django 4.2.3 on 2025-01-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_address_user_birthday_user_civil_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jobs',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
