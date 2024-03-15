from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from .assignment import *
from statistics import median
from .datelist import datelist


class Transactions(APIView):
    def get(self, request):
        categories_string = request.query_params.get('categories', None)
        categories = categories_string.split('%') if categories_string else []
        datefrom = request.query_params.get('datefrom', None)
        dateto = request.query_params.get('dateto', None).replace('/', '')

        print("api call:", categories, datefrom, dateto)
        filters = {}
        if categories:
            filters['category__name__in'] = categories
        if datefrom and datefrom != 'null':
            filters['date__gte'] = datefrom
        if dateto and dateto != 'null':
            filters['date__lte'] = dateto

        data = Transaction.objects.filter(**filters).order_by('-date')
        serializer = TransactionSerializer(data, many=True)

        return Response(status=200, data=serializer.data)

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            createBindingByTransactions(serializer.instance)
            return Response(status=200, data="Transactions have been uploaded")
        return Response(status=500, data="Transactions could not be uploaded")

    def put(self, request):
        print("DATA", request.data)
        data = request.data
        transaction = Transaction.objects.get(id=data['id'])

        if 'category' in data:
            data['category'] = Category.objects.get(name=data['category']).id
            if transaction.category == None:
                data['overruled'] = True
            elif transaction.category.id != data['category']:
                data['overruled'] = True

        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Transaction has been updated")
        return Response(status=500, data="Transaction could not be updated")

    def delete(self, request):
        data = request.data
        Transaction.objects.filter(id=data['id']).delete()
        return Response(status=200, data="Transaction has been deleted")


class TransactionsWithoutCategory(APIView):
    def get(self, request):
        try:
            data = Transaction.objects.filter(category=None)
            serializer = TransactionSerializer(data, many=True)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Transactions could not be queried")


class TransactionUnlock(APIView):
    def put(self, request):
        data = request.data
        transaction = Transaction.objects.get(id=data['id'])
        transaction.overruled = False
        assignment = transaction.assignments.first()
        if assignment:
            transaction.category = assignment.category
        else:
            transaction.category = None
        transaction.save()
        return Response(status=200, data="Transaction has been updated")


class Statistics(APIView):
    def get(self, request):
        data = []
        dateto = request.query_params.get('dateto', None)
        dateto = dateto.replace('/', '') if dateto else None
        datefrom = request.query_params.get('datefrom', None)

        dates = datelist(datefrom, dateto)
        print("dates", dates)
        if dates == []:
            return Response(status=400, data="Invalid date range")

        categories = Category.objects.all()
        for category in categories:
            entry = {}

            # Statistics
            entry['category'] = category.name
            entry['sum'] = round(Transaction.objects.filter(
                category=category).aggregate(Sum('amount'))['amount__sum'], 2)
            entry['average'] = round(Transaction.objects.filter(category=category).aggregate(
                Avg('amount'))['amount__avg'], 2)
            amounts = list(Transaction.objects.filter(
                category=category).values_list('amount', flat=True))
            entry['median'] = round(median(amounts) if amounts else None, 2)

            data.append(entry)

        return Response(status=200, data=data)


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


class AssignmentsConflicts(APIView):
    def get(self, request):
        transactionConflicts = Transaction.objects.annotate(
            num_assignments=Count('assignments')).filter(num_assignments__gt=1)
        assignments = Assignment.objects.filter(
            transaction__in=transactionConflicts).values_list('id', flat=True).distinct()
        return Response(status=200, data=assignments)
