from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from encrypted_model_fields.fields import EncryptedCharField, EncryptedDateField, EncryptedIntegerField, EncryptedDateTimeField, EncryptedBooleanField


class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    fileName = EncryptedCharField(max_length=100, null=True)
    fileDate = EncryptedDateTimeField(null=True)
    uploadID = models.UUIDField(null=True)
    date = models.DateField(null=True, blank=True)
    amount = EncryptedIntegerField(null=True, blank=True)
    recipient = EncryptedCharField(max_length=100, null=True, blank=True)
    description = EncryptedCharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    assignments = models.ManyToManyField(
        'Assignment', related_name='transaction', blank=True, default=None)
    overruled = EncryptedBooleanField(default=False)


class Setting(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    currency = models.CharField(max_length=1, default='€')
    locale = models.CharField(max_length=5, default='de-DE')
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
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    name = EncryptedCharField(max_length=100)
    color = EncryptedCharField(max_length=7, default='#444444')


class Assignment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    keyword = EncryptedCharField(max_length=100)
    checkMode = EncryptedCharField(max_length=100)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=False)
