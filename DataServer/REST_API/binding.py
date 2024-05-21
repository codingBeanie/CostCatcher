from .models import *
from django.db.models import Q
import logging
import datetime
import calendar


def assignTransaction(transaction, prevData=None, reevaluate=False):
    log = logging.getLogger('utils')
    try:
        assignment = findAssignment(transaction)
        user = transaction.user
        # CASE: transaction is new, no prevData
        if not prevData and reevaluate == False:
            if assignment:
                transaction.assignment = assignment
                transaction.category = assignment.category
                transaction.save()

                statistic = Statistic.objects.get_or_create(user=user,
                                                            period=transaction.period, category=transaction.category)
                statistic[0].amount += transaction.amount

        # CASE: transaction is updated or assignment is updated
        else:
            # for checks, find the previous assignment. might be None, if assignment was deleted, or none was set
            prevAssignment = transaction.assignment

            # assign new assignment to transaction
            if assignment:
                transaction.assignment = assignment
                if transaction.overruled == False:
                    transaction.category = assignment.category
                transaction.save()
            else:
                transaction.assignment = None
                if transaction.overruled == False:
                    transaction.category = None
                transaction.save()

            # find statistic for old assignment
            if prevAssignment:
                prevPeriod = Period.objects.get(id=prevData['period'])
                prevStatistic = Statistic.objects.get(
                    user=user, period=prevPeriod, category=prevAssignment.category)
                prevStatistic.amount -= prevData['amount']
                prevStatistic.save()

            # find statistic for new assignment
            if transaction.category:
                newStatistic = Statistic.objects.get_or_create(
                    user=user, period=transaction.period, category=transaction.category)
                newStatistic[0].amount += transaction.amount
                newStatistic.save()

        log.debug(f"{transaction}, {assignment}, {
                  transaction.category}, {transaction.overruled}")

    except Exception as e:
        log.error(f"Error in assignTransaction: {e}")


def findAssignment(transaction):
    log = logging.getLogger('utils')
    try:
        user = transaction.user
        assignments = Assignment.objects.filter(user=user)
        for assignment in assignments:
            # Check-Mode: recipient_only
            if assignment.checkMode == "recipient_only":
                if assignment.keyword.lower() in transaction.recipient.lower():
                    return assignment

            # Check-Mode: description_only
            elif assignment.checkMode == "description_only":
                if assignment.keyword.lower() in transaction.description.lower():
                    return assignment

            # Check-Mode: recipient_and_description
            elif assignment.checkMode == "recipient_and_description":
                if assignment.keyword.lower() in transaction.recipient.lower() and assignment.keyword.lower() in transaction.description.lower():
                    return assignment

            # Check-Mode: recipient_or_description
            elif assignment.checkMode == "recipient_or_description":
                if assignment.keyword.lower() in transaction.recipient.lower() or assignment.keyword.lower() in transaction.description.lower():
                    return assignment

    except Exception as e:
        log.error(f"Error in createBindingByTransactions: {e}")
        return None


def createPeriods(fromYear, toYear):
    log = logging.getLogger('utils')
    try:
        # check if period already exists
        firstPeriod = Period.objects.filter(year=fromYear, month=1)
        lastPeriod = Period.objects.filter(year=toYear, month=12)
        if firstPeriod and lastPeriod:
            return

        # create periods
        for year in range(fromYear, toYear + 1):
            for month in range(1, 13):
                quarter = ((month - 1) // 3) + 1
                fromDate = datetime.date(year, month, 1)
                _, lastDay = calendar.monthrange(year, month)
                toDate = datetime.date(year, month, lastDay)

                Period.objects.create(
                    year=year,
                    month=month,
                    quarter=quarter,
                    fromDate=fromDate,
                    toDate=toDate)

    except Exception as e:
        log.error(f"Error in createPeriods: {e}")
