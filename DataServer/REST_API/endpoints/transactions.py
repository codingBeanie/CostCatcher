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
        log = logging.getLogger('api')
        try:
            requestID = request.query_params.get('id', None)
            requestCategory = request.query_params.get('category', None)

            filters = {}
            filters['user'] = request.user.id
            if requestID:
                filters['id'] = requestID
            if requestCategory:
                if requestCategory == '0':
                    filters['category'] = None
                else:
                    filters['category'] = requestCategory

            transactions = Transaction.objects.filter(
                **filters)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(status=200, data=serializer.data)

        except Exception as e:
            log.error(f"Error in Transactions API (GET): {e}")
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

            prevData = {"amount": transaction.amount,
                        "period": transaction.period.id}
            # check if category has been changed and set overruled to true
            log.debug(f"{transaction.category}, {data['category']}")
            if transaction.category and data['category']:
                if transaction.category.id != data['category']:
                    transaction.overruled = True
            else:
                transaction.overruled = True

            serializer = TransactionSerializer(transaction, data=data)
            if serializer.is_valid():
                serializer.save()

                # re-evaluate assignment and category

                assignTransaction(transaction, prevData=prevData)
                return Response(status=200, data="Transaction has been updated")
            return Response(status=400, data=serializer.errors)

        except Exception as e:
            print("Error in Transactions API (PUT):", e)
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
