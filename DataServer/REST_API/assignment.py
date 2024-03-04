from .models import Assignment, Category, Transaction
from django.db.models import Q


def createBinding(assignment):
    keyword = assignment['keyword']
    category = assignment['category']
    checkRecipient = assignment['checkRecipient']
    checkDescription = assignment['checkDescription']
    print("Keyword: ", keyword)
    print("Category: ", category)
    print("Check Recipient: ", checkRecipient)
    print("Check Description: ", checkDescription)

    # Recipient True / Description True
    if checkRecipient and checkDescription:
        transactions = Transaction.objects.filter(
            recipient__icontains=keyword)

        print(transactions)
        for transaction in transactions:
            print(transaction.recipient, transaction.description)
