from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Transaction
from .serializer import *
from rest_framework.views import APIView


class Transactions(APIView):
    def get(self, request):
        data = Transaction.objects.all()
        serializer = TransactionSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Files(APIView):
    def get(self, request):
        data = Transaction.objects.values('fileID', 'fileName', 'fileDate')
        distinct_data = list({item['fileID']: item for item in data}.values())
        return Response(distinct_data)

    def delete(self, request):
        data = request.data
        fileID = data['id']
        Transaction.objects.filter(fileID=fileID).delete()
        return Response(status=204)
