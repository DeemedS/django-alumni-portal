# Generated by Django 4.2.3 on 2024-09-07 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_student_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]