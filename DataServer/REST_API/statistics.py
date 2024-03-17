from .models import *
from django.db.models import Sum
from statistics import mean, median


def createStatisticsObject(category, dates):
    entry = {}
    entry['Category'] = category.name if category else 'None'

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
    income['Category'] = 'Income'
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
    expenses['Category'] = 'Expenses'
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
    net['Category'] = 'Net'
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
