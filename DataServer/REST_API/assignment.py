from .models import Assignment, Category, Transaction
from django.db.models import Q


def createBinding(assignment):
    keyword = assignment['keyword']
    category = assignment['category']
    checkRecipient = assignment['checkRecipient']
    checkDescription = assignment['checkDescription']

    # Recipient True / Description True
    if checkRecipient and checkDescription:
        transactions = Transaction.objects.filter(
            Q(recipient__icontains=keyword) & Q(description__icontains=keyword))

        for transaction in transactions:
            print(transaction.recipient, transaction.description)
