from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Statistic
from ..serializer import FileSerializer
import datetime
import logging


class Files(APIView):
    def get(self, request):
        try:
            user = request.user.id
            uuids = Transaction.objects.filter(
                user=user).values('uploadID').distinct()
            result = []
            for uuid in uuids:
                transactions = Transaction.objects.filter(
                    user=user, uploadID=uuid['uploadID']).order_by('date')

                example = transactions.first()
                count = transactions.count()

                entry = {}
                entry['fileName'] = example.fileName
                entry['fileDate'] = example.fileDate
                entry['uploadID'] = example.uploadID
                entry['count'] = count
                entry['dateRange'] = str(transactions.first(
                ).date) + " - " + str(transactions.last().date)

                result.append(entry)
            return Response(status=200, data=result)
        except Exception as e:
            print("Error in Files API:", e)
            return Response(status=500, data="Files could not be queried")

    def delete(self, request):
        log = logging.getLogger('api')
        try:
            filters = {'user': request.user.id,
                       'uploadID': request.data}
            transactions = Transaction.objects.filter(**filters)

            # clear the statistics before deleting the transactions
            for transaction in transactions:
                if transaction.category:
                    statistic = Statistic.objects.get(
                        user=request.user, category=transaction.category, period=transaction.period)
                    statistic.amount -= transaction.amount
                    statistic.save()

            transactions.delete()
            return Response(status=200, data="File has been deleted")

        except Exception as e:
            log.error(f"Error in Files DELETE API: {e}")
            return Response(status=500, data="File could not be deleted")
