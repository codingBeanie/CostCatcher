# Generated by Django 5.0.2 on 2024-04-17 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0034_alter_transaction_uploadid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(),
        ),
    ]
