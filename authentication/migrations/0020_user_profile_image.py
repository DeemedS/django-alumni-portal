# Generated by Django 4.2.3 on 2025-03-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_alter_user_civil_status_alter_user_middle_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='user/profile_pics/default.jpg', null=True, upload_to='user/profile_pics/'),
        ),
    ]
