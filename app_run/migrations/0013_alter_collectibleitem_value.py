# Generated by Django 5.2 on 2025-05-31 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0012_alter_collectibleitem_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectibleitem',
            name='value',
            field=models.IntegerField(),
        ),
    ]
