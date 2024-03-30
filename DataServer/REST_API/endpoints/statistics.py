from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Category
from ..datelist import datelist
from django.db.models import Sum
from statistics import mean, median


class Statistics(APIView):
    def get(self, request):
        data = []
        dateto = request.query_params.get('dateto', None)
        datefrom = request.query_params.get('datefrom', None)

        # produces [{'month-year': '01-2021', 'datefrom': '2021-01-01', 'dateto': '2021-01-31'}, ...]
        dates = datelist(datefrom, dateto)

        if dates == []:
            return Response(status=400, data="Invalid date range")

        # Period/Category statistics
        categories = Category.objects.all()
        for category in categories:
            data.append(createStatisticsObject(category, dates))

        # if transactions have no category, create a category 'UNDEFINED'/NONE
        if Transaction.objects.filter(category=None).exists():
            data.append(createStatisticsObject(None, dates))

        data = sorted(data, key=lambda x: x['Sum'], reverse=True)

        # Totals
        totals = createStatisticsTotals(dates)
        for total in totals:
            data.append(total)

        return Response(status=200, data=data)


def createStatisticsObject(category, dates):
    entry = {}
    categoryName = category.name if category else 'UNDEFINED'
    categoryID = category.id if category else 0
    categoryColor = category.color if category else '#444444'

    entry['Category'] = {'name': categoryName,
                         'id': categoryID, 'color': categoryColor}

    sumlist = []
    # monthly statistics
    for daterange in dates:
        filters = {'category': category,
                   'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto']}
        try:
            entry[daterange['month-year']] = round(Transaction.objects.filter(**filters).aggregate(
                Sum('amount'))['amount__sum'], 0)
            sumlist.append(entry[daterange['month-year']])
        except:
            entry[daterange['month-year']] = 0
            sumlist.append(0)

    # Statistics
    entry['Sum'] = sum(sumlist)
    entry['Average'] = round(mean(sumlist), 0)
    entry['Median'] = round(median(sumlist), 0)

    return entry


def createStatisticsTotals(dates):
    totals = []

    # INCOME
    income = {}
    incomeList = []
    income['Category'] = {'name': 'Income', 'id': -1, 'color': '#444444'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto'],
                   'amount__gte': 0}
        try:
            income[daterange['month-year']] = round(Transaction.objects.filter(**filters).aggregate(
                Sum('amount'))['amount__sum'], 0)
            incomeList.append(income[daterange['month-year']])
        except:
            income[daterange['month-year']] = 0
            incomeList.append(0)
    income['Sum'] = sum(incomeList)
    income['Average'] = round(mean(incomeList), 0)
    income['Median'] = round(median(incomeList), 0)

    # Expenses
    expenses = {}
    expensesList = []
    expenses['Category'] = {'name': 'Expenses', 'id': -2, 'color': '#444444'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto'],
                   'amount__lt': 0}
        try:
            expenses[daterange['month-year']] = round(Transaction.objects.filter(**filters).aggregate(
                Sum('amount'))['amount__sum'], 0)
            expensesList.append(expenses[daterange['month-year']])
        except:
            expenses[daterange['month-year']] = 0
            expensesList.append(0)
    expenses['Sum'] = sum(expensesList)
    expenses['Average'] = round(mean(expensesList), 0)
    expenses['Median'] = round(median(expensesList), 0)

    # NET
    net = {}
    netList = []
    net['Category'] = {'name': 'Net', 'id': -3, 'color': '#444444'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto']}
        try:
            net[daterange['month-year']] = round(Transaction.objects.filter(**filters).aggregate(
                Sum('amount'))['amount__sum'], 0)
            netList.append(net[daterange['month-year']])
        except:
            net[daterange['month-year']] = 0
            netList.append(0)
    net['Sum'] = sum(netList)
    net['Average'] = round(mean(netList), 0)
    net['Median'] = round(median(netList), 0)

    totals.append(income)
    totals.append(expenses)
    totals.append(net)
    return totals
