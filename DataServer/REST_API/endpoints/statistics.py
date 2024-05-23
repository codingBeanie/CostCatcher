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
            return Response(status=200, data="Statistics GET")

        except Exception as e:
            self.log.error("API ERROR [statistics/GET]:", e)
            return Response(status=500, data="Error in Statistics GET")
