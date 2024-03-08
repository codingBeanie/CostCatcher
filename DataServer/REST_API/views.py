from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from .assignment import *


class Transactions(APIView):
    def get(self, request):
        try:
            data = Transaction.objects.all()
            serializer = TransactionSerializer(data, many=True)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Transactions could not be queried")

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Transactions have been uploaded")
        return Response(status=500, data="Transactions could not be uploaded")


class TransactionsWithoutCategory(APIView):
    def get(self, request):
        try:
            data = Transaction.objects.filter(category=None)
            serializer = TransactionSerializer(data, many=True)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Transactions could not be queried")


class Files(APIView):
    def get(self, request):
        try:
            data = Transaction.objects.values(
                'fileName', 'fileDate').distinct()
            return Response(status=200, data=data)
        except:
            return Response(status=500, data="Files could not be queried")

    def delete(self, request):
        try:
            data = request.data
            fileName = data['fileName']
            fileDate = data['fileDate']
            Transaction.objects.filter(
                fileName=fileName, fileDate=fileDate).delete()
            return Response(status=200, data="File has been deleted")
        except:
            return Response(status=500, data="File could not be deleted")


class Schema(APIView):
    def get(self, request):
        try:
            data = ImportSchema.objects.first()
            serializer = ImportSchemaSerializer(data)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Schema could not be queried")

    def put(self, request):
        data = request.data
        schema = ImportSchema.objects.first()
        serializer = ImportSchemaSerializer(schema, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Schema has been updated")
        return Response(status=500, data="Schema could not be updated")


class Categories(APIView):
    def get(self, request):
        try:
            data = Category.objects.all()
            serializer = CategorySerializer(data, many=True)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Categories could not be queried")

    def post(self, request):
        data = request.data
        if Category.objects.filter(name=data['name']).exists():
            return Response(status=400, data="Category already exists")

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been created")
        return Response(status=500, data="Category could not be created")

    def put(self, request):
        data = request.data
        print(data)
        category = Category.objects.get(id=data['id'])
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been updated")
        return Response(status=500, data="Category could not be updated")

    def delete(self, request):
        try:
            data = request.data
            name = data['name']
            Category.objects.filter(name=name).delete()
            return Response(status=200, data="Category has been deleted")
        except:
            return Response(status=500, data="Category could not be deleted")


class Assignments(APIView):
    def get(self, request):
        try:
            data = Assignment.objects.all()
            serializer = AssignmentSerializer(data, many=True)
            for assignment in serializer.data:
                assignment['category'] = Category.objects.get(
                    id=assignment['category']).name
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Assignments could not be queried")

    def post(self, request):
        try:
            data = request.data
            keyword = data['keyword']
            data['category'] = Category.objects.get(name=data['category']).id

            if Assignment.objects.filter(keyword=keyword).exists():
                return Response(status=400, data="Assignment already exists")

            serializer = AssignmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                createBinding(serializer.instance)
                return Response(status=200, data="Assignment has been created")

        except:
            return Response(status=500, data="Assignment could not be created")

    def put(self, request):
        data = request.data
        assignment = Assignment.objects.get(id=data['id'])
        deleteBinding(assignment)
        assignment.keyword = data['keyword']
        assignment.checkRecipient = data['checkRecipient']
        assignment.checkDescription = data['checkDescription']
        assignment.category = Category.objects.get(name=data['category'])
        assignment.save()
        createBinding(assignment)
        return Response(status=200, data="Assignment has been updated")

    def delete(self, request):
        data = request.data
        assignment = Assignment.objects.get(id=data['id'])
        deleteBinding(assignment)
        assignment.delete()
        return Response(status=200, data="Assignment has been deleted")
