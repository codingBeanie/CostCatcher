# Generated by Django 5.0.2 on 2024-03-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0007_remove_importschema_valuetype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='importschema',
            name='dateFormat',
            field=models.CharField(default='DD.MM.YYYY', max_length=100),
        ),
    ]
