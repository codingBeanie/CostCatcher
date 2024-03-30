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

        # Totals
        totals = createStatisticsTotals(dates)
        for total in totals:
            data.append(total)

        return Response(status=200, data=data)


def createStatisticsObject(category, dates):
    item = {}
    categoryName = category.name if category else 'UNDEFINED'
    categoryID = category.id if category else 0
    categoryColor = category.color if category else '#444444'

    item['Category'] = {'name': categoryName,
                        'id': categoryID, 'color': categoryColor}

    sumlist = []
    # monthly statistics
    for daterange in dates:
        filters = {'category': category,
                   'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto']}
        monthlySum = Transaction.objects.filter(
            **filters).aggregate(Sum('amount'))['amount__sum']

        if monthlySum is not None:
            sumlist.append(monthlySum)
            item[daterange['month-year']] = monthlySum
        else:
            item[daterange['month-year']] = 0

    # Statistics
    itemSum = sum(sumlist)
    itemAverage = mean(sumlist) if len(sumlist) > 1 else sum(sumlist)
    itemMedian = median(sumlist) if len(sumlist) > 1 else 0
    item['Statistics'] = {'Sum': itemSum,
                          'Average': itemAverage, 'Median': itemMedian}
    return item


def createStatisticsTotals(dates):
    totals = []

    # INCOME
    income = {}
    incomeList = []
    income['Category'] = {'name': 'Income', 'id': -1, 'color': '#005403'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto'],
                   'amount__gte': 0}
        monthlySum = Transaction.objects.filter(
            **filters).aggregate(Sum('amount'))['amount__sum']
        if monthlySum is not None:
            income[daterange['month-year']] = monthlySum
            incomeList.append(monthlySum)
        else:
            income[daterange['month-year']] = 0
    incomeSum = sum(incomeList)
    incomeAverage = mean(incomeList) if len(
        incomeList) > 1 else sum(incomeList)
    incomeMedian = median(incomeList) if len(incomeList) > 1 else 0
    income['Statistics'] = {'Sum': incomeSum,
                            'Average': incomeAverage, 'Median': incomeMedian}

    # Expenses
    expenses = {}
    expensesList = []
    expenses['Category'] = {'name': 'Expenses', 'id': -2, 'color': '#540000'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto'],
                   'amount__lt': 0}
        monthlySum = Transaction.objects.filter(
            **filters).aggregate(Sum('amount'))['amount__sum']
        if monthlySum is not None:
            expenses[daterange['month-year']] = monthlySum
            expensesList.append(monthlySum)
        else:
            expenses[daterange['month-year']] = 0

    expensesSum = sum(expensesList)
    expensesAverage = mean(expensesList) if len(
        expensesList) > 1 else sum(expensesList)
    expensesMedian = median(expensesList) if len(expensesList) > 1 else 0
    expenses['Statistics'] = {'Sum': expensesSum,
                              'Average': expensesAverage, 'Median': expensesMedian}

    # NET
    net = {}
    netList = []
    net['Category'] = {'name': 'Net', 'id': -3, 'color': '#111111'}
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto']}
        monthlySum = Transaction.objects.filter(
            **filters).aggregate(Sum('amount'))['amount__sum']
        if monthlySum is not None:
            net[daterange['month-year']] = monthlySum
            netList.append(monthlySum)
        else:
            net[daterange['month-year']] = 0

    netSum = sum(netList)
    netAverage = mean(netList) if len(netList) > 1 else sum(netList)
    netMedian = median(netList) if len(netList) > 1 else 0
    net['Statistics'] = {'Sum': netSum,
                         'Average': netAverage, 'Median': netMedian}

    totals.append(income)
    totals.append(expenses)
    totals.append(net)
    return totals
