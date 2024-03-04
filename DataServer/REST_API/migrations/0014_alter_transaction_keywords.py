# Generated by Django 5.0.2 on 2024-03-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0013_transaction_keywords_transaction_overruled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='keywords',
            field=models.ManyToManyField(blank=True, default=None, related_name='transaction', to='REST_API.assignment'),
        ),
    ]
