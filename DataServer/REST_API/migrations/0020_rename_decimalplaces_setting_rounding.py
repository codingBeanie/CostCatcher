# Generated by Django 5.0.2 on 2024-03-19 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0019_rename_settings_setting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='decimalPlaces',
            new_name='rounding',
        ),
    ]