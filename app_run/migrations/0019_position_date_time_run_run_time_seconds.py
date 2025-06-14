# Generated by Django 5.2 on 2025-06-01 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0018_collectibleitem_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='run_time_seconds',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
