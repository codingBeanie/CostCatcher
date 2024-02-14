from django.shortcuts import render
from rest_framework import generics
from .models import Transaction
from .serializer import *
from rest_framework.views import APIView


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class FilesList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().values(
        'sourceFile', 'sourceFileDate').distinct()
    serializer_class = FilesSerializer


class FilesDelete(APIView):
    def post(self, request):
        file = request.data['file']
        Transaction.objects.filter(sourceFile=file).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
