from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
import calendar
import datetime


class Datespan(APIView):
    def get(self, request):
        try:
            transactions = Transaction.objects.filter(user=request.user.id)
            print(transactions.count())
            last_date = transactions.order_by('date').last().date
            print(last_date)
            default_last = datetime.date(last_date.year, last_date.month, calendar.monthrange(
                last_date.year, last_date.month)[1])

            first_date = transactions.order_by('date').first().date
            print(first_date)
            default_first = datetime.date(first_date.year, first_date.month, 1)
            if (default_last - default_first > datetime.timedelta(days=365)):
                default_first = default_last - datetime.timedelta(days=365)
                default_first = datetime.date(
                    default_first.year, default_first.month, 1)

            data = {
                'defaultFirst': default_first,
                'defaultLast': default_last
            }
            return Response(status=200, data=data)
        except Exception as e:
            print("Error in Datespan API:", e)
            return Response(status=500, data="No data found")
