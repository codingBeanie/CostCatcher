from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction
import calendar
import datetime


class Datespan(APIView):
    def get(self, request):
        last_date = Transaction.objects.order_by('date').last().date
        default_last = datetime.date(last_date.year, last_date.month, calendar.monthrange(
            last_date.year, last_date.month)[1])

        first_date = Transaction.objects.order_by('date').first().date
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
