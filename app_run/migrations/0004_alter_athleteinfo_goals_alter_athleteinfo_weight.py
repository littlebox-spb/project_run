# Generated by Django 5.2 on 2025-05-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0003_athleteinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleteinfo',
            name='goals',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='athleteinfo',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
