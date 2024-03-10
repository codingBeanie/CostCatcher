from .models import Assignment, Category, Transaction
from django.db.models import Q


def createBinding(assignment):
    # Recipient True / Description False
    if assignment.checkRecipient and not assignment.checkDescription:
        transactions = Transaction.objects.filter(
            recipient__icontains=assignment.keyword)

    # Recipient False / Description True
    elif not assignment.checkRecipient and assignment.checkDescription:
        transactions = Transaction.objects.filter(
            description__icontains=assignment.keyword)

    # Recipient True / Description True
    elif assignment.checkRecipient and assignment.checkDescription:
        transactions = Transaction.objects.filter(
            Q(recipient__icontains=assignment.keyword) | Q(description__icontains=assignment.keyword))

    for transaction in transactions:
        if transaction.overruled == False and transaction.category == None:
            transaction.category = assignment.category

    for transaction in transactions:
        transaction.assignments.add(assignment.id)
        transaction.save()
    return


def deleteBinding(assignment):
    transactions = Transaction.objects.filter(
        assignments__keyword=assignment.keyword)

    for transaction in transactions:
        transaction.assignments.remove(assignment.id)
        transaction.save()

        if transaction.overruled == False and transaction.assignments.all().count() > 0:
            lastAssignment = transaction.assignments.last()
            transaction.category = Category.objects.get(
                id=lastAssignment.category.id)
        else:
            transaction.category = None

        transaction.save()
    return


def createBindingByTransactions(transactions):
    for transaction in transactions:
        for assignment in Assignment.objects.all():
            # Recipient True / Description False
            if assignment.checkRecipient and not assignment.checkDescription:
                if assignment.keyword.lower() in transaction.recipient.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

            # Recipient False / Description True
            elif not assignment.checkRecipient and assignment.checkDescription:
                if assignment.keyword.lower() in transaction.description.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

            # Recipient True / Description True
            elif assignment.checkRecipient and assignment.checkDescription:
                if assignment.keyword.lower() in transaction.recipient.lower() and assignment.keyword.lower() in transaction.description.lower():
                    transaction.category = assignment.category
                    transaction.assignments.add(assignment.id)

        transaction.save()
    return
