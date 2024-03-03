from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Transaction, ImportSchema, Category
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
        data = Transaction.objects.values('fileName', 'fileDate').distinct()
        print(data)
        return Response(data)

    def delete(self, request):
        data = request.data
        fileName = data['fileName']
        fileDate = data['fileDate']
        try:
            Transaction.objects.filter(
                fileName=fileName, fileDate=fileDate).delete()
            return Response(status=204)
        except:
            return Response(status=400)


class Schema(APIView):
    def get(self, request):
        data = ImportSchema.objects.all()
        serializer = ImportSchemaSerializer(data, many=True)
        return Response(serializer.data)

    def put(self, request):
        data = request.data
        schema = ImportSchema.objects.first()
        serializer = ImportSchemaSerializer(schema, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Categories(APIView):
    def get(self, request):
        data = Category.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data)
        if Category.objects.filter(name=data['name']).exists():
            return Response(status=400, data="Category already exists")

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        data = request.data
        oldName = data['oldName']
        name = data['newName']
        transactionType = data['newType']
        category = Category.objects.get(name=oldName)
        category.name = name
        category.transactionType = transactionType
        category.save()
        return Response(status=201, data="Category updated")

    def delete(self, request):
        data = request.data
        name = data['name']
        try:
            Category.objects.filter(name=name).delete()
            return Response(status=204, data="Category deleted")
        except:
            return Response(status=400, data="Category does not exist")
