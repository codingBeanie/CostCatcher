# Generated by Django 5.0.2 on 2024-04-09 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0026_delete_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='colAmount',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='setting',
            name='colDate',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='colDescription',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='setting',
            name='colRecipient',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='setting',
            name='dateFormat',
            field=models.CharField(default='DD.MM.YYYY', max_length=100),
        ),
        migrations.AddField(
            model_name='setting',
            name='decimalSeparator',
            field=models.CharField(default=',', max_length=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='delimiter',
            field=models.CharField(default=';', max_length=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='rowFirst',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='rowLast',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='setting',
            name='thousandsSeparator',
            field=models.CharField(default='.', max_length=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]