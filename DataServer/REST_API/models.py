from django.db import models


class Transaction(models.Model):
    sourceFile = models.CharField(max_length=100)
    sourceFileDate = models.DateTimeField()
    date = models.DateTimeField()
    amount = models.FloatField()
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
