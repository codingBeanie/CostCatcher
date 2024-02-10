from django.shortcuts import render
from rest_framework import generics
from .models import Transaction
from .serializer import *


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class FilesList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().values(
        'sourceFile', 'sourceFileDate').distinct()
    serializer_class = FilesSerializer
