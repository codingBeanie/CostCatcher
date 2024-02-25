from django.db import models


class Transaction(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    fileDate = models.DateTimeField(null=True)
    fileID = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    amount = models.FloatField()
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


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
