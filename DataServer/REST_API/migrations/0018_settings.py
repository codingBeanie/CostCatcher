# Generated by Django 5.0.2 on 2024-03-19 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0017_alter_transaction_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(default='€', max_length=1)),
                ('decimalPlaces', models.IntegerField(default=0)),
            ],
        ),
    ]
