from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
from ..serializer import FileSerializer
import datetime


class Files(APIView):
    def get(self, request):
        try:
            user = request.user.id
            transactions = Transaction.objects.filter(
                user=user).values('fileName', 'fileDate', 'uploadID')
            uniqueEntries = []
            # because i can not query a .distinct() on encrypted fields
            # i have to iterate through the decrypted values and append them to a list
            for transaction in transactions:
                if transaction not in uniqueEntries:
                    uniqueEntries.append(transaction)
            return Response(status=200, data=uniqueEntries)
        except Exception as e:
            print("Error in Files API:", e)
            return Response(status=500, data="Files could not be queried")

    def delete(self, request):
        try:
            filters = {'user': request.user.id,
                       'uploadID': request.data}
            transactions = Transaction.objects.filter(**filters)
            transactions.delete()
            return Response(status=200, data="File has been deleted")
        except:
            return Response(status=500, data="File could not be deleted")
