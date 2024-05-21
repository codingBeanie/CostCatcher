from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
from ..serializer import TransactionSerializer
from ..binding import *
import calendar
import datetime
import uuid
import logging


class Transactions(APIView):

    def get(self, request):
        try:
            # Query parameters
            queryID = request.query_params.get('id', None)
            queryID = None if queryID == 'null' else queryID
            category = request.query_params.get('category', None)
            category = None if category == 'null' else category
            period = request.query_params.get('period', None)
            period = None if period == 'null' else period

            # Filters
            filters = {}
            amountFilterMode = None

            if queryID:
                filters['id'] = queryID

            # CATEGORY
            # NONE = no filter, show all
            if category:
                # 0 = no category, show all without category
                if int(category) == 0:
                    filters['category'] = None

                # -1 = INCOME
                if int(category) == -1:
                    amountFilterMode = 'income'

                # -2 = EXPENSE
                if int(category) == -2:
                    amountFilterMode = 'expense'

                # filter to valid category
                if int(category) > 0:
                    filters['category__id'] = category

            # PERIOD
            if period:
                fromDate = datetime.datetime(
                    int(period[0:4]), int(period[5:7]), 1)
                lastDay = calendar.monthrange(fromDate.year, fromDate.month)[1]
                toDate = datetime.datetime(
                    fromDate.year, fromDate.month, lastDay)
                filters['date__gte'] = fromDate
                filters['date__lte'] = toDate

            transactions = Transaction.objects.filter(user=request.user.id)
            # this just works for non-enctypted fields
            transactions = transactions.filter(**filters)
            # amount field is encrypted, so we have to filter it manually
            if amountFilterMode:
                for transaction in transactions:
                    if transaction.amount < 0:
                        if amountFilterMode == 'income':
                            transactions = transactions.exclude(
                                id=transaction.id)
                    else:
                        if amountFilterMode == 'expense':
                            transactions = transactions.exclude(
                                id=transaction.id)

            result = TransactionSerializer(transactions, many=True).data
            return Response(status=200, data=result)

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transactions could not be queried")


####################################################################################################
# PUT
####################################################################################################

    def post(self, request):
        log = logging.getLogger('api')
        try:
            data = request.data
            dates = []
            # add additional data
            for item in data:
                item['user'] = request.user.id
                item['uploadID'] = uuid.uuid5(
                    uuid.NAMESPACE_DNS, item['fileName'] + item['fileDate'])
                dates.append(int(item['date'].split('-')[0]))

            # check period range
            createPeriods(min(dates), max(dates))

            # assign a period to each item
            for item in data:
                item['period'] = Period.objects.get(
                    year=int(item['date'].split('-')[0]), month=int(item['date'].split('-')[1])).id

            # check serializer and save
            serializer = TransactionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()

                # each new Transaction has to be checked for a valid assignment rule
                for instance in serializer.instance:
                    assignTransaction(instance)
                return Response(status=200, data="Transactions have been uploaded")

            else:
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            log.error(f"Error in Transactions API (POST): {e}")
            return Response(status=500, data="Transactions could not be uploaded")


####################################################################################################
# PUT
####################################################################################################

    def put(self, request):
        log = logging.getLogger('api')
        try:
            data = request.data
            user = request.user
            data['user'] = user.id
            data['amount'] = int(float(data['amount']) * 100)
            transaction = Transaction.objects.get(id=data['id'], user=user)

            # check if category has been changed and set overruled to true
            if transaction.category and data['category']:
                if transaction.category.id != data['category']:
                    transaction.overruled = True
            else:
                transaction.overruled = True

            # if overruled set to false
            if 'overruled' in data.keys():
                if transaction.overruled == True and data['overruled'] == False:
                    data['overruled'] = False
                    if transaction.assignments.first():
                        data['category'] = transaction.assignments.first().category.id
                    else:
                        data['category'] = None

            serializer = TransactionSerializer(transaction, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200, data="Transaction has been updated")
            return Response(status=400, data=serializer.errors)

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transaction could not be updated")

    def delete(self, request):
        try:
            data = request.data
            user = request.user
            Transaction.objects.filter(id=data, user=user).delete()
            return Response(status=200, data="Transaction has been deleted")
        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transaction could not be deleted")
