# Generated by Django 5.0.2 on 2024-04-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0033_alter_transaction_uploadid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='uploadID',
            field=models.UUIDField(null=True),
        ),
    ]
