# Generated by Django 5.0.3 on 2024-04-14 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0006_remove_presentmeeting_allowed_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentmeeting',
            name='participants',
            field=models.TextField(default=''),
        ),
    ]
