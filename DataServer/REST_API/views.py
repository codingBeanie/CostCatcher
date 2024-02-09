from django.shortcuts import render
from rest_framework import generics
from .models import Transaction
from .serializer import TransactionSerializer

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

