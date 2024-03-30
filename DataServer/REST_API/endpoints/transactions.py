from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
from ..serializer import TransactionSerializer
from ..bindings import createBindingByTransactions


class Transactions(APIView):

    def get(self, request):
        try:
            categories = request.query_params.get('categories', None)
            filters = {}
            if categories == "[0]":
                filters['category__isnull'] = True
            elif categories:
                filters['category__id__in'] = categories
            # Get query parameters
            # categories_string = request.query_params.get('categories', None)
            # special_categories = categories_string if categories_string == 'Income' or categories_string == 'Expenses' or categories_string == 'Net' else None
            # categories_string = "" if special_categories else categories_string
            # categories = categories_string.split(
            #     '%') if categories_string else []
            # datefrom = request.query_params.get('datefrom', None)
            # dateto = request.query_params.get('dateto', None).replace('/', '')

            # # Filtering
            # filters = {}
            # if categories:
            #     filters['category__name__in'] = categories
            # if special_categories == 'Income':
            #     filters['amount__gte'] = 0
            # if special_categories == 'Expenses':
            #     filters['amount__lt'] = 0
            # if datefrom and datefrom != 'null':
            #     filters['date__gte'] = datefrom
            # if dateto and dateto != 'null':
            #     filters['date__lte'] = dateto

            data = Transaction.objects.filter(**filters).order_by('-date')
            serializer = TransactionSerializer(data, many=True)

            return Response(status=200, data=serializer.data)

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transactions could not be queried")

    def post(self, request):
        try:
            data = request.data
            serializer = TransactionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                createBindingByTransactions(serializer.instance)
                return Response(status=200, data="Transactions have been uploaded")
            else:
                return Response(status=400, data="Error in data format")

        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transactions could not be uploaded")

    def put(self, request):
        try:
            data = request.data
            transaction = Transaction.objects.get(id=data['id'])

            if 'category' in data:
                data['category'] = Category.objects.get(
                    name=data['category']).id
                if transaction.category == None:
                    data['overruled'] = True
                elif transaction.category.id != data['category']:
                    data['overruled'] = True

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
            Transaction.objects.filter(id=data).delete()
            return Response(status=200, data="Transaction has been deleted")
        except Exception as e:
            print("Error in Transactions API:", e)
            return Response(status=500, data="Transaction could not be deleted")
