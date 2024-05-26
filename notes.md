# Use Cases
* Import of new transactions
* delete transaction
* edit transaction value
* new assignment rule
* changed assignment rule
    * delete assignment rule
    * new assignment rule
* override assignment rule

# Model Transaction
* user
* $fileName
* $fileDate
* uploadID - uuid
* $date
* $amount
* $description
* $recipient
* FK-one assignments
* FK-one periods (2024-Q1-1)
* FK-one category
* overrule

# Model Period
* month
* month-name
* quarter
* year

# Category
* name

# Statistic
* FK-one category
* FK-one period
* $amount

# NEW TRANSACTION
for each transaction:
    check assignment.keywords => 
        set transaction.category
        if category:
            statistics?category&period+=amount

# DELETE TRANSACTION
statistics?category=transaction.category -= transaction.amount

# CHANGED TRANSACTION
statistics?category=transaction.category -= transaction.amountOLD
statistics?category=transaction.category += transaction.amountNEW

# NEW ASSIGNMENT RULE
for each transaction.assignment=null && transaction.override=false:
    transaction.assignment=newAssignment
    transaction.category=newAssignment.Category

# DELETE ASSIGNMENT RULE
for each transaction.assignment=deleteAssignment:
    if override:
        just remove assignment
    else:
        searchfornewAssignment()

# override
just set override and override-category

# override unlock
unset override and searchfornewAssignment(transaction)

searchfornewAssignment(transaction)
for each assignment:
    check for match:
        transaction.assignment + transaction.category
    
# functions
categoryCashier(category, period, amount)



