# Generated by Django 5.0.2 on 2024-02-21 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sourceFileDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
