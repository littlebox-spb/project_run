# Generated by Django 5.2 on 2025-05-29 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0007_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='distance',
            field=models.FloatField(default=0),
        ),
    ]
