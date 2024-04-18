from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Category
from ..datelist import datelist
from django.db.models import Sum
from statistics import mean, median
from datetime import datetime


class Statistics(APIView):
    def get(self, request):
        data = []
        dateto = request.query_params.get('dateto', None)
        datefrom = request.query_params.get('datefrom', None)
        user = request.user.id
        transactions = Transaction.objects.filter(user=user)

        # produces [{'month-year': '01-2021', 'datefrom': '2021-01-01', 'dateto': '2021-01-31'}, ...]
        dates = datelist(datefrom, dateto)

        if dates == []:
            return Response(status=400, data="Invalid date range")

        # Period/Category statistics
        categories = Category.objects.filter(user=request.user.id)
        for category in categories:
            data.append(createStatisticsObject(category, dates, user))

        # if transactions have no category, create a category 'UNDEFINED'/NONE
        if transactions.filter(category=None).exists():
            data.append(createStatisticsObject(None, dates, user))

        # Sorting
        sortColumn = request.query_params.get('sortcolumn', None)
        sortAsc = request.query_params.get('sortasc', None)
        sortAsc = True if sortAsc == 'true' else False
        if sortColumn == 'Category':
            data.sort(key=lambda x: x['Category']['name'], reverse=sortAsc)
        else:
            data.sort(key=lambda x: x[sortColumn], reverse=sortAsc)

        # Totals
        totals = createStatisticsTotals(dates, user)
        for total in totals:
            data.append(total)

        return Response(status=200, data=data)


def createStatisticsObject(category, dates, user):
    item = {}
    categoryName = category.name if category else 'UNDEFINED'
    categoryID = category.id if category else 0
    categoryColor = category.color if category else '#444444'

    item['Category'] = {'name': categoryName,
                        'id': categoryID, 'color': categoryColor}

    sumlist = []

    # monthly statistics
    for daterange in dates:
        dateFrom = datetime.strptime(daterange['datefrom'], '%Y-%m-%d').date()
        dateTo = datetime.strptime(daterange['dateto'], '%Y-%m-%d').date()
        filters = {'user': user, 'date__gte': dateFrom, 'date__lte': dateTo}
        transactions = Transaction.objects.filter(**filters)
        monthlySum = 0
        for transaction in transactions:
            if transaction.category == category:
                monthlySum += transaction.amount / 100

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


def createStatisticsTotals(dates, user):
    totals = []

    # Preparation
    income = {}
    incomeDateRange = []
    incomeList = []
    income['Category'] = {'name': 'Income', 'id': -1, 'color': '#005403'}

    expenses = {}
    expensesList = []
    expenseDateRange = []
    expenses['Category'] = {'name': 'Expenses', 'id': -2, 'color': '#540000'}

    net = {}
    netList = []
    netDateRange = []
    net['Category'] = {'name': 'Net', 'id': -3, 'color': '#111111'}

    # collect data
    for daterange in dates:
        filters = {'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto'],
                   'user': user}
        transactions = Transaction.objects.filter(
            **filters)
        for transaction in transactions:
            value = transaction.amount / 100
            # INCOME
            if value >= 0:
                incomeList.append(value)
                incomeDateRange.append(value)
            # EXPENSES
            else:
                expensesList.append(value)
                expenseDateRange.append(value)
            # NET
            netList.append(value)
            netDateRange.append(value)

        income[daterange['month-year']] = sum(incomeDateRange)
        expenses[daterange['month-year']] = sum(expenseDateRange)
        net[daterange['month-year']] = sum(netDateRange)

    # in case of no data
    if len(incomeList) == 0:
        incomeList.append(0)
    if len(expensesList) == 0:
        expensesList.append(0)
    if len(netList) == 0:
        netList.append(0)

    # Statistics
    incomeSum = sum(incomeList)
    incomeAverage = mean(incomeList) if len(
        incomeList) > 1 else sum(incomeList)
    incomeMedian = median(incomeList) if len(incomeList) > 1 else 0
    income['Statistics'] = {'Sum': incomeSum,
                            'Average': incomeAverage, 'Median': incomeMedian}

    expensesSum = sum(expensesList)
    expensesAverage = mean(expensesList) if len(
        expensesList) > 1 else sum(expensesList)
    expensesMedian = median(expensesList) if len(expensesList) > 1 else 0
    expenses['Statistics'] = {'Sum': expensesSum,
                              'Average': expensesAverage, 'Median': expensesMedian}

    netSum = sum(netList)
    netAverage = mean(netList) if len(netList) > 1 else sum(netList)
    netMedian = median(netList) if len(netList) > 1 else 0
    net['Statistics'] = {'Sum': netSum,
                         'Average': netAverage, 'Median': netMedian}

    totals.append(income)
    totals.append(expenses)
    totals.append(net)

    print(totals)
    return totals
