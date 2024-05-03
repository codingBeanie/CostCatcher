from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction, Category
from ..datelist import datelist
from django.db.models import Sum
from statistics import mean, median
from datetime import datetime


class Statistics(APIView):
    def get(self, request):
        try:
            data = []
            dateto = request.query_params.get('dateto', None)
            datefrom = request.query_params.get('datefrom', None)
            showTotals = request.query_params.get(
                'showTotals', True)  # categories, totals, all
            filtermode = request.query_params.get(
                'filtermode', 'all')  # only income, expenses or all
            showStatistics = request.query_params.get('statistics', False)
            user = request.user.id
            transactions = Transaction.objects.filter(user=user)

            # produces [{'month-year': '01-2021', 'datefrom': '2021-01-01', 'dateto': '2021-01-31'}, ...]
            dates = datelist(datefrom, dateto)
            if dates == []:
                return Response(status=400, data="Invalid date range")

            ####################################################################################################
            # Period/Category statistics
            categories = Category.objects.filter(user=request.user.id)
            for category in categories:
                item = createStatisticsObject(
                    category, dates, user, filtermode, showStatistics)
                if item:
                    data.append(item)

            # if transactions have no category, create a category 'UNDEFINED'/NONE
            if transactions.filter(category=None).exists():
                item = createStatisticsObject(
                    None, dates, user, filtermode, showStatistics)
                if item:
                    data.append(item)

            ####################################################################################################
            # Totals
            if showTotals == 'true' or showTotals == True:
                totals = createStatisticsTotals(dates, user)
                for total in totals:
                    data.append(total)

            return Response(status=200, data=data)
        except Exception as e:
            print("Error in Statistics GET: ", e)
            return Response(status=500, data="Can not get the data.")


def createStatisticsObject(category, dates, user, filtermode, showStatistics):
    item = {}
    categoryName = category.name if category else 'UNDEFINED'
    categoryID = category.id if category else 0
    categoryColor = category.color if category else '#444444'

    item['Category'] = {'name': categoryName,
                        'id': categoryID, 'color': categoryColor}
    item['Data'] = {}

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
                if filtermode == 'income':
                    if transaction.amount >= 0:
                        monthlySum += transaction.amount / 100
                elif filtermode == 'expense':
                    if transaction.amount < 0:
                        monthlySum += transaction.amount / 100
                else:
                    monthlySum += transaction.amount / 100

        # if no transactions are found, set monthlySum to 0
        if monthlySum is not None:
            sumlist.append(monthlySum)
            item['Data'][daterange['month-year']] = monthlySum
        else:
            item['Data'][daterange['month-year']] = 0

    # Statistics
    if showStatistics or showStatistics == 'true':
        itemSum = sum(sumlist)
        itemAverage = mean(sumlist) if len(sumlist) > 1 else sum(sumlist)
        itemMedian = median(sumlist) if len(sumlist) > 1 else 0
        item['Statistics'] = {'Sum': itemSum,
                              'Average': itemAverage, 'Median': itemMedian}

    # check for each filtermode if item is 0, if so, return None
    if filtermode == "income" and sum(sumlist) <= 0 or filtermode == "expense" and sum(sumlist) >= 0:
        return None
    return item


def createStatisticsTotals(dates, user):
    totals = []

    # Preparation
    income = {}
    incomeDateRange = []
    incomeList = []
    income['Category'] = {'name': 'Income', 'id': -1, 'color': '#005403'}
    income['Data'] = {}

    expenses = {}
    expensesList = []
    expenseDateRange = []
    expenses['Category'] = {'name': 'Expenses', 'id': -2, 'color': '#540000'}
    expenses['Data'] = {}

    net = {}
    netList = []
    netDateRange = []
    net['Category'] = {'name': 'Net', 'id': -3, 'color': '#111111'}
    net['Data'] = {}

    # collect data
    for daterange in dates:
        expenseDateRange = []
        incomeDateRange = []
        netDateRange = []
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

        income['Data'][daterange['month-year']] = sum(incomeDateRange)
        expenses['Data'][daterange['month-year']] = sum(expenseDateRange)
        net['Data'][daterange['month-year']] = sum(netDateRange)

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

    return totals
