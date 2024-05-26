from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Category, Period
from ..datelist import datelist
from django.db.models import Sum
from statistics import mean, median
from datetime import datetime
import logging

# STATISTICS RESPONSE
# [ {   'Period': {'title':2021-01, 'year': 2021, 'month': 1, 'quarter': 1},
#       'Category': {'name': 'UNDEFINED', 'id': 0, 'color': '#444444'},
#       'Data': {0, 0},
#       'Statistics': {'Sum': 0, 'Average': 0, 'Median': 0} }, ... ]


class Statistics(APIView):
    log = logging.getLogger("api")

    def get(self, request):
        try:
            # ****************************************************************************************************#
            # *** PARAMETERS ***#

            # get parameters from request
            periodMode = request.query_params.get('periodmode', 'monthly')
            valueMode = request.query_params.get('valuemode', None)
            fromYear = request.query_params.get('fromyear', None)
            toYear = request.query_params.get('toyear', None)
            fromPeriod = request.query_params.get('fromperiod', None)
            toPeriod = request.query_params.get('toperiod', None)
            user = request.user.id

            # check if null and get default value
            if fromYear is None or fromYear == 'null' or fromYear == 'undefined':
                fromYear = Period.objects.filter(
                    user=user).order_by('year').first().year

            if toYear is None or toYear == 'null' or toYear == 'undefined':
                toYear = Period.objects.filter(
                    user=user).order_by('year').first().year

            if fromPeriod is None or fromPeriod == 'null' or fromPeriod == 'undefined':
                fromPeriodYear = Period.objects.filter(
                    user=user).order_by('year').first().year
                fromPeriodMonth = 1
            else:
                fromPeriodYear = int(fromPeriod.split('-')[0])
                fromPeriodMonth = int(fromPeriod.split('-')[1])

            if toPeriod is None or toPeriod == 'null' or toPeriod == 'undefined':
                toPeriodYear = Period.objects.filter(
                    user=user).order_by('year').first().year
                toPeriodMonth = 1
            else:
                toPeriodYear = int(toPeriod.split('-')[0])
                toPeriodMonth = int(toPeriod.split('-')[1])

            # ****************************************************************************************************#
            # *** PERIODS ***#

            periods = []

            # MODES: monthly, quarterly, yearly
            if periodMode != 'single':
                for year in range(int(fromYear), int(toYear) + 1):

                    if periodMode == 'monthly':
                        for month in range(1, 13):
                            entry = {}
                            period = Period.objects.get(
                                user=user, year=year, month=month)
                            entry['title'] = f"{period.year}-{period.month}"
                            entry['year'] = period.year
                            entry['month'] = period.month
                            periods.append(entry)

                    if periodMode == 'quarterly':
                        for quarter in range(1, 5):
                            entry = {}
                            period = Period.objects.filter(
                                user=user, year=year, quarter=quarter).order_by('month')
                            entry['title'] = f"{
                                period[0].year}-Q{period[0].quarter}"
                            entry['year'] = period[0].year
                            entry['quarter'] = period[0].quarter
                            periods.append(entry)

                    if periodMode == 'yearly':
                        entry = {}
                        period = Period.objects.filter(
                            user=user, year=year).values('year').distinct().order_by('year')
                        for p in period:
                            entry['title'] = f"{p['year']}"
                            entry['year'] = p['year']
                            periods.append(entry)

            # MODE: single
            if periodMode == 'single':
                entry = {}
                filters = {}
                filters['user'] = user
                filters['year__gte'] = fromPeriodYear
                filters['year__lte'] = toPeriodYear
                filters['month__gte'] = fromPeriodMonth
                filters['month__lte'] = toPeriodMonth

                period = Period.objects.filter(**filters)
                for p in period:
                    entry['title'] = f"{p.year}-{p.month}"
                    entry['year'] = p.year
                    entry['month'] = p.month
                    periods.append(entry)

            # self.log.debug(f"Statistics GET: periods={periods}")
            # ****************************************************************************************************#
            # *** CATEGORIES ***#

            categories = []
            categoriesQueried = Category.objects.filter(user=user)
            for category in categoriesQueried:
                entry = {}
                entry['name'] = category.name
                entry['id'] = category.id
                entry['color'] = category.color
                categories.append(entry)

            # add UNDEFINED category
            entry = {}
            entry['name'] = 'UNDEFINED'
            entry['id'] = 0
            entry['color'] = '#444444'
            categories.append(entry)
            # self.log.debug(f"Statistics GET: categories={categories}")

            # ****************************************************************************************************#
            # *** CONSTRUCTION AND DATA ***#

            data = []
            sumData = {}
            for category in categories:
                # setup
                entry = {}
                entry['Category'] = category
                entry['Period'] = periods
                entry['Data'] = []
                entry['Statistics'] = {}

                # fill data
                for period in periods:
                    # set sumData
                    if period['title'] not in sumData:
                        sumData[period['title']] = 0

                    # filter
                    filters = {}
                    filters['user'] = user
                    filters['category'] = category['id']
                    if filters['category'] == 0:
                        filters['category'] = None

                    # periodmode filter
                    if periodMode != 'yearly':
                        filters['period__year'] = period['year']
                        filters['period__month'] = period['month']

                    if periodMode == 'yearly':
                        filters['period__year'] = period['year']

                    # valuemode filter
                    if valueMode == 'income':
                        filters['amount__gte'] = 0

                    if valueMode == 'expense':
                        filters['amount__lt'] = 0

                    # get transactions
                    transactions = Transaction.objects.filter(**filters)
                    amount = transactions.aggregate(
                        Sum('amount'))['amount__sum']
                    if amount is None:
                        amount = 0
                    else:
                        amount = amount / 100
                        sumData[period['title']] += amount

                    entry['Data'].append(amount)

                # statistics
                sumlist = entry['Data']
                allZero = all(x == 0 for x in sumlist)
                # only if there are values add statistics and append to data
                if not allZero:
                    entry['Statistics']['Sum'] = sum(sumlist)
                    entry['Statistics']['Average'] = mean(sumlist)
                    entry['Statistics']['Median'] = median(sumlist)
                    data.append(entry)

            # ****************************************************************************************************#
            # sort data by sumvalue
            data = sorted(
                data, key=lambda x: x['Statistics']['Sum'], reverse=True if valueMode == 'income' else False)
            response = {'data': data, 'sumData': sumData}
            return Response(status=200, data=response)

        except Exception as e:
            self.log.error("API ERROR [statistics/GET]:", e)
            return Response(status=500, data="Error in Statistics GET")
