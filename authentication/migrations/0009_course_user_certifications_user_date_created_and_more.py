# Generated by Django 4.2.3 on 2025-02-27 11:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_user_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('course_name', models.CharField(max_length=120)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='certifications',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='licenses',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='user',
            name='section',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='events',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='user',
            name='jobs',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_code', models.CharField(max_length=10, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='authentication.course')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.course'),
        ),
    ]
