from .models import Assignment, Category, Transaction
from django.db.models import Q


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


def createBindingByTransactions(transactions):
    for transaction in transactions:
        user = transaction.user
        assignments = Assignment.objects.filter(user=user)
        for assignment in assignments:
            # Check-Mode: recipient_only
            if assignment.checkMode == "recipient_only":
                if assignment.keyword.lower() in transaction.recipient.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

            # Check-Mode: description_only
            elif assignment.checkMode == "description_only":
                if assignment.keyword.lower() in transaction.description.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

            # Check-Mode: recipient_and_description
            elif assignment.checkMode == "recipient_and_description":
                if assignment.keyword.lower() in transaction.recipient.lower() and assignment.keyword.lower() in transaction.description.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

            # Check-Mode: recipient_or_description
            elif assignment.checkMode == "recipient_or_description":
                if assignment.keyword.lower() in transaction.recipient.lower() or assignment.keyword.lower() in transaction.description.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

        transaction.save()
    return
