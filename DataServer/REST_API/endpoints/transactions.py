from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
from ..serializer import TransactionSerializer
from ..bindings import createBindingByTransactions
import calendar
import datetime
import uuid


class Transactions(APIView):

    def get(self, request):
        try:
            # Query parameters
            queryID = request.query_params.get('id', None)
            category = request.query_params.get('category', None)
            period = request.query_params.get('period', None)

            # Filters
            filters = {}

            # CATEGORY
            # NONE = no filter, show all
            if category:
                # 0 = no category, show all without category
                if int(category) == 0:
                    filters['category'] = None

                # -1 = INCOME
                if int(category) == -1:
                    filters['amount__gte'] = 0

                # -2 = EXPENSE
                if int(category) == -2:
                    filters['amount__lt'] = 0

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

            # because the fields are encrypted, i need to apply the filters manually
            transactions = Transaction.objects.filter(user=request.user.id)
            transactions = transactions.filter(**filters)
            result = TransactionSerializer(transactions, many=True).data

            return Response(status=200, data=result)

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transactions could not be queried")

    def post(self, request):
        try:
            data = request.data
            for item in data:
                item['user'] = request.user.id
                item['uploadID'] = uuid.uuid5(
                    uuid.NAMESPACE_DNS, item['fileName'] + item['fileDate'])

            serializer = TransactionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                createBindingByTransactions(serializer.instance)
                return Response(status=200, data="Transactions have been uploaded")
            else:
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transactions could not be uploaded")

    def put(self, request):
        try:
            data = request.data
            user = request.user
            transaction = Transaction.objects.get(id=data['id'], user=user)

            # if category changed, set overrule attribute
            if transaction.category != data['category']:
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
            return Response(status=400, data="Error with the data format")

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
