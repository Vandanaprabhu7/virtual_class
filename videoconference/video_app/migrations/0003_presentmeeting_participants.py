# Generated by Django 5.0.3 on 2024-04-03 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0002_presentmeeting_onprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentmeeting',
            name='participants',
            field=models.TextField(default='[]'),
        ),
    ]
