from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from .bindings import *
from .datelist import datelist
from .statistics import createStatisticsObject, createStatisticsTotals


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

        if dates == []:
            return Response(status=400, data="Invalid date range")

        # Period/Category statistics
        categories = Category.objects.all()
        for category in categories:
            data.append(createStatisticsObject(category, dates))
        data.append(createStatisticsObject(None, dates))

        data = sorted(data, key=lambda x: x['Sum'], reverse=True)

        # Totals
        totals = createStatisticsTotals(dates)
        for total in totals:
            data.append(total)

        return Response(status=200, data=data)


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


class AssignmentsConflicts(APIView):
    def get(self, request):
        transactionConflicts = Transaction.objects.annotate(
            num_assignments=Count('assignments')).filter(num_assignments__gt=1)
        assignments = Assignment.objects.filter(
            transaction__in=transactionConflicts).values_list('id', flat=True).distinct()
        return Response(status=200, data=assignments)


class Settings(APIView):
    def get(self, request):
        data = Setting.objects.first()
        serializer = SettingsSerializer(data)
        return Response(status=200, data=serializer.data)

    def put(self, request):
        data = request.data
        settings = Setting.objects.first()
        serializer = SettingsSerializer(settings, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Settings have been updated")
        return Response(status=500, data="Settings could not be updated")
