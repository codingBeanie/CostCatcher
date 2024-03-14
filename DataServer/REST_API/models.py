from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Transaction(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    fileDate = models.DateTimeField(null=True)
    date = models.DateField()
    amount = models.FloatField()
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    assignments = models.ManyToManyField(
        'Assignment', related_name='transaction', blank=True, default=None)
    overruled = models.BooleanField(default=False)


class ImportSchema(models.Model):
    rowFirst = models.IntegerField(default=1)
    rowLast = models.IntegerField(default=0)
    colDate = models.IntegerField(default=1)
    colRecipient = models.IntegerField(default=2)
    colDescription = models.IntegerField(default=3)
    colAmount = models.IntegerField(default=4)
    delimiter = models.CharField(max_length=1, default=';')
    thousandsSeparator = models.CharField(max_length=1, default='.')
    decimalSeparator = models.CharField(max_length=1, default=',')
    dateFormat = models.CharField(max_length=100, default='DD.MM.YYYY')


class Category(models.Model):
    name = models.CharField(max_length=100)


class Assignment(models.Model):
    keyword = models.CharField(max_length=100)
    checkRecipient = models.BooleanField(default=False)
    checkDescription = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)


@receiver(post_migrate)
def create_default_entry(sender, **kwargs):
    ImportSchema.objects.get_or_create()
