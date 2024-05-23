from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Category
from ..datelist import datelist
from django.db.models import Sum
from statistics import mean, median
from datetime import datetime
import logging


class Statistics(APIView):
    log = logging.getLogger("api")

    def get(self, request):
        try:
            periodMode = request.query_params.get('periodmode', 'monthly')
            fromYear = request.query_params.get('fromyear', None)
            toYear = request.query_params.get('toyear', None)
            self.log.debug(f"Statistics GET: periodMode={
                periodMode}, fromYear={fromYear}, toYear={toYear}")

            return Response(status=200, data="")

        except Exception as e:
            self.log.error("API ERROR [statistics/GET]:", e)
            return Response(status=500, data="Error in Statistics GET")
