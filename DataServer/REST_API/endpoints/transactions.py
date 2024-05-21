from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import TransactionSerializer
from ..bindings import createBindingByTransactions
import calendar
import datetime
import uuid
import logging
from ..periods import createPeriods


class Transactions(APIView):
    log = logging.getLogger("api")
    ####################################################################################################
    # GET
    ####################################################################################################

    def get(self, request):
        try:
            # Query parameters
            queryID = request.query_params.get('id', None)
            queryCategory = request.query_params.get('category', None)
            queryYear = request.query_params.get('year', None)
            queryMonth = request.query_params.get('month', None)
            queryQuarter = request.query_params.get('quarter', None)

            # Validate query parameters
            queryID = None if queryID == 'null' else queryID
            category = None if queryCategory == 'null' else queryCategory
            year = None if queryYear == 'null' else queryYear
            month = None if queryMonth == 'null' else queryMonth
            quarter = None if queryQuarter == 'null' else queryQuarter

            # Filters
            filters = {}
            filters['user'] = request.user.id
            if queryID:
                filters['id'] = queryID

            # CATEGORY
            # NONE = no filter, show all
            if category:
                # 0 = no category, show all without category
                if int(category) == 0:
                    filters['category'] = None

                # filter to valid category
                if int(category) > 0:
                    filters['category__id'] = category

            # PERIOD
            if year:
                filters['period__year'] = year
            if month:
                filters['period__month'] = month
            if quarter:
                filters['period__quarter'] = quarter

            transactions = Transaction.objects.filter(**filters)
            result = TransactionSerializer(transactions, many=True)
            return Response(status=200, data=result.data)

        except Exception as e:
            self.log.error("API ERROR [transaction/GET]:", e)
            return Response(status=500, data="Transactions could not be queried")

####################################################################################################
# POST
####################################################################################################
    def post(self, request):
        try:
            data = request.data
            dates = []
            for item in data:
                item['user'] = request.user.id
                item['uploadID'] = uuid.uuid5(
                    uuid.NAMESPACE_DNS, item['fileName'] + item['fileDate'])
                dates.append(int(item['date'].split('-')[0]))

            # check period range
            createPeriods(request.user, min(dates), max(dates))

            # assign a period to each item
            for item in data:
                item['period'] = Period.objects.get(
                    year=int(item['date'].split('-')[0]), month=int(item['date'].split('-')[1])).id

            serializer = TransactionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                createBindingByTransactions(serializer.instance)
                return Response(status=200, data="Transactions have been uploaded")
            else:
                self.log.error(
                    "API ERROR [transaction/POST]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [transaction/POST]:", e)
            return Response(status=500, data="Transactions could not be uploaded")

####################################################################################################
# PUT
####################################################################################################
    def put(self, request):
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

            # check if date has changed and set period
            if transaction.date != data['date']:
                newYear = int(data['date'].split('-')[0])
                newMonth = int(data['date'].split('-')[1])
                # make sure period exists
                checkPeriod = Period.objects.filter(
                    user=user, year=newYear, month=newMonth)

                # if period does not exist, create it
                if checkPeriod:
                    data['period'] = checkPeriod.first().id
                else:
                    createPeriods(user, newYear, newYear)
                    period = Period.objects.get(
                        user=user, year=newYear, month=newMonth)
                    data['period'] = period.id

            serializer = TransactionSerializer(transaction, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200, data="Transaction has been updated")
            else:
                self.log.error(
                    "API ERROR [transaction/PUT]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [transaction/PUT]:", e)
            return Response(status=500, data="Transaction could not be updated")

####################################################################################################
# DELETE
####################################################################################################
    def delete(self, request):
        try:
            data = request.data
            user = request.user
            Transaction.objects.filter(id=data, user=user).delete()
            return Response(status=200, data="Transaction has been deleted")
        except Exception as e:
            self.log.error("API ERROR [transaction/DELETE]:", e)
            return Response(status=500, data="Transaction could not be deleted")
