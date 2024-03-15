from .models import *
from django.db.models import Count, Sum, Avg


def createStatisticsObject(category, dates):
    entry = {}
    entry['category'] = category.name if category else 'None'

    # monthly statistics
    for daterange in dates:
        filters = {'category': category,
                   'date__gte': daterange['datefrom'],
                   'date__lte': daterange['dateto']}
        try:
            entry[daterange['month-year']] = round(Transaction.objects.filter(**filters).aggregate(
                Sum('amount'))['amount__sum'], 2)
        except:
            entry[daterange['month-year']] = 0

    # Statistics
    entry['sum'] = round(Transaction.objects.filter(
        category=category).aggregate(Sum('amount'))['amount__sum'], 2)

    return entry
