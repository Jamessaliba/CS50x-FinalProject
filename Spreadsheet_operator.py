
import os
import pandas as pd

# Replace these with your existing implementations.
def get_expense():
#expense sheet
    worksheet_expense = pd.read_csv('Expenses_sheet.csv', header=None)
    expenserows = worksheet_expense[1:]
    return expenserows
    
def get_revenue():
#revenue sheet
    worksheet_revenue = pd.read_csv('Revenue_sheet.csv', header=None)
    revenuerows = worksheet_revenue[1:]
    return revenuerows

def cata_totals_count(data, month):

    total = {}
    count = {}

    for index, value in data.iterrows():
        try:
            category = value[3]
            if value[6].split("/")[1] == month:
                amount = float(value[2].replace("$", ""))
                total.setdefault(category, 0)
                count.setdefault(category + " count", 0)

                total[category] += amount
                count[category + " count"] += 1
        except ValueError:
            continue

    return total, count

def monthly_sheet_totals_count(data, month):
    total = 0
    count = 0

    for value in data:
        try:
            if value[6].split("/")[1] == month:
                amount = float(value[2].replace("$", ""))
                total += amount
                count += 1
        except ValueError:
            continue

    return total, count

def spent_month(month):
    data = get_expense()
    total_spent = 0
    for index, row in data.iterrows():
        row_month = str(row[6]).split('/')[1]
        if row[3] == 'Unnecessary' or row[3] == 'Restaurant':   
            if month == row_month:
             total_spent += float(row[2].replace('$',''))
    return total_spent

if __name__ == "__main__":
    expense = get_expense()