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


class AssignmentsConflicts(APIView):
    def get(self, request):
        transactionConflicts = Transaction.objects.annotate(
            num_assignments=Count('assignments')).filter(num_assignments__gt=1)
        assignments = Assignment.objects.filter(
            transaction__in=transactionConflicts).values_list('id', flat=True).distinct()
        return Response(status=200, data=assignments)
