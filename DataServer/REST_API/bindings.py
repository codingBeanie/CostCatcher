from .models import *
from django.db.models import Q
import logging
import datetime
import calendar


def createBinding(assignment):
    userTransactions = Transaction.objects.filter(user=assignment.user)
    transactions = []
    # Check-Mode: recipient_only
    if assignment.checkMode == "recipient_only":
        for transaction in userTransactions:
            if assignment.keyword.lower() in transaction.recipient.lower():
                transactions.append(transaction)

    # Check-Mode: description_only
    elif assignment.checkMode == "description_only":
        for transaction in userTransactions:
            if assignment.keyword.lower() in transaction.description.lower():
                transactions.append(transaction)

    # Check-Mode: recipient_and_description
    elif assignment.checkMode == "recipient_and_description":
        for transaction in userTransactions:
            if assignment.keyword.lower() in transaction.recipient.lower() and assignment.keyword.lower() in transaction.description.lower():
                transactions.append(transaction)

    # Check-Mode: recipient_or_description
    elif assignment.checkMode == "recipient_or_description":
        for transaction in userTransactions:
            if assignment.keyword.lower() in transaction.recipient.lower() or assignment.keyword.lower() in transaction.description.lower():
                transactions.append(transaction)

    # add category to transactions if not overruled
    for transaction in transactions:
        if transaction.overruled == False and transaction.category == None:
            transaction.category = assignment.category

    # add assignment to transactions
    for transaction in transactions:
        transaction.assignments.add(assignment.id)
        transaction.save()
    return


def deleteBinding(assignment):
    userTransactions = Transaction.objects.filter(user=assignment.user)
    userTransactions = userTransactions.filter(
        Q(assignments__id=assignment.id))

    for transaction in userTransactions:
        transaction.assignments.remove(assignment.id)
        transaction.save()
        if transaction.assignments.count() > 0 and transaction.overruled == False:
            transaction.category = transaction.assignments.first().category
            transaction.save()
        elif transaction.assignments.count() == 0 and transaction.overruled == False:
            transaction.category = None
            transaction.save()
    assignment.delete()
    return


####################################################################################################
# Find a assignment by keyword and assign category to transaction
####################################################################################################

def findAndBindAssignment(transactions):
    log = logging.getLogger('utils')
    try:
        for transaction in transactions:
            user = transaction.user
            assignments = Assignment.objects.filter(user=user)
            for assignment in assignments:
                # Check-Mode: recipient_only
                if assignment.checkMode == "recipient_only":
                    if assignment.keyword.lower() in transaction.recipient.lower():
                        updateTransactionAssignment(transaction, assignment)
                        break

                # Check-Mode: description_only
                elif assignment.checkMode == "description_only":
                    if assignment.keyword.lower() in transaction.description.lower():
                        updateTransactionAssignment(transaction, assignment)
                        break

                # Check-Mode: recipient_and_description
                elif assignment.checkMode == "recipient_and_description":
                    if assignment.keyword.lower() in transaction.recipient.lower() and assignment.keyword.lower() in transaction.description.lower():
                        updateTransactionAssignment(transaction, assignment)
                        break

                # Check-Mode: recipient_or_description
                elif assignment.checkMode == "recipient_or_description":
                    if assignment.keyword.lower() in transaction.recipient.lower() or assignment.keyword.lower() in transaction.description.lower():
                        updateTransactionAssignment(transaction, assignment)
                        break

    except Exception as e:
        log.error(f"Error in createBindingByTransactions: {e}")


####################################################################################################
# Save Assignment to Transaction and increase statistic counter
####################################################################################################
def updateTransactionAssignment(transaction, assignment, prevTransaction=None):
    log = logging.getLogger('utils')
    try:
        # CASE: transaction is new, no assignments
        if prevTransaction == None:
            transaction.assignment = assignment
            transaction.category = assignment.category
            transaction.save()

            statistic = Statistic.objects.get(
                period=transaction.period, category=transaction.category)
            statistic.amount += transaction.amount

        # CASE: transaction has changed in a way
        if prevTransaction:
            pass

    except Exception as e:
        log.error(f"Error in updateTransactionAssignment: {e}")

    return


def createPeriods(fromYear, toYear):
    log = logging.getLogger('utils')
    try:
        # check if period already exists
        firstPeriod = Period.objects.get(year=fromYear, month=1)
        lastPeriod = Period.objects.get(year=toYear, month=12)
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
