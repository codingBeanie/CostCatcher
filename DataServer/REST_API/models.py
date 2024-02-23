from django.db import models


class Transaction(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    fileDate = models.DateTimeField(null=True)
    fileID = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    amount = models.FloatField()
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
