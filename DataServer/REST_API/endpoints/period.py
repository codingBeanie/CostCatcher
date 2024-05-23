from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializer import PeriodSerializer
from ..models import Transaction, Period
import calendar
import datetime
import logging


class PeriodDefault(APIView):
    log = logging.getLogger("api")
    # returns a year (latest year) for the default period selection

    def get(self, request):
        try:
            period = Period.objects.filter(
                user=request.user.id).order_by('year').first()
            serializer = PeriodSerializer(period)
            return Response(status=200, data=serializer.data)

        except Exception as e:
            self.log.error("API ERROR [SelectPeriod/GET]:", e)
            return Response(status=500, data="Error in SelectPeriod GET")


class PeriodList(APIView):
    log = logging.getLogger("api")
    # returns a list of all years with transactions

    def get(self, request):
        try:
            user = request.user.id
            years = Period.objects.filter(user=user).values(
                'year').distinct().order_by('year')
            years = [item['year'] for item in years]
            return Response(status=200, data=years)

        except Exception as e:
            self.log.error("API ERROR [SelectPeriod/GET]:", e)
            return Response(status=500, data="Error in SelectPeriod GET")
