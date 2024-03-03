from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Transaction(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    fileDate = models.DateTimeField(null=True)
    date = models.DateTimeField()
    amount = models.FloatField()
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)


class ImportSchema(models.Model):
    rowFirst = models.IntegerField(default=1)
    rowLast = models.IntegerField(default=0)
    colDate = models.IntegerField(default=1)
    colRecipient = models.IntegerField(default=1)
    colDescription = models.IntegerField(default=1)
    colAmount = models.IntegerField(default=1)
    delimiter = models.CharField(max_length=1, default=';')
    thousandsSeparator = models.CharField(max_length=1, default='.')
    decimalSeparator = models.CharField(max_length=1, default=',')
    dateFormat = models.CharField(max_length=100, default='DD.MM.YYYY')


class Category(models.Model):
    name = models.CharField(max_length=100)
    transactionType = models.CharField(
        max_length=100, null=True, default="Expense")


@receiver(post_migrate)
def create_default_entry(sender, **kwargs):
    ImportSchema.objects.get_or_create()
