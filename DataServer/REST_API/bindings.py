from .models import Assignment, Category, Transaction
from django.db.models import Q


def createBinding(assignment):

    # Check-Mode: recipient_only
    if assignment.checkMode == "recipient_only":
        transactions = Transaction.objects.filter(
            recipient__icontains=assignment.keyword)

    # Check-Mode: description_only
    elif assignment.checkMode == "description_only":
        transactions = Transaction.objects.filter(
            description__icontains=assignment.keyword)

    # Check-Mode: recipient_and_description
    elif assignment.checkMode == "recipient_and_description":
        transactions = Transaction.objects.filter(
            Q(recipient__icontains=assignment.keyword) & Q(description__icontains=assignment.keyword))

    # Check-Mode: recipient_or_description
    elif assignment.checkMode == "recipient_or_description":
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
