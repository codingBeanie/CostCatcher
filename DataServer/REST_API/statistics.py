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
                Sum('amount'))['amount__sum'], 2)
            sumlist.append(entry[daterange['month-year']])
        except:
            entry[daterange['month-year']] = 0
            sumlist.append(0)

    # Statistics
    entry['Sum'] = round(Transaction.objects.filter(
        category=category).aggregate(Sum('amount'))['amount__sum'], 2)
    entry['Average'] = round(mean(sumlist), 2)
    entry['Median'] = round(median(sumlist), 2)

    return entry
