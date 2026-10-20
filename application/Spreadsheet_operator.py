import pandas as pd
from pathlib import Path
import os

def set_dir():
    current_directory = Path(__file__).resolve().parent
    project_directory = current_directory.parent
    csv_directory = project_directory / "CSV_files"
    os.chdir(csv_directory)

def get_expense():
#expense sheet
    set_dir()
    worksheet_expense = pd.read_csv('Expenses_sheet.csv', header=None)
    expenserows = worksheet_expense[1:]
    return expenserows
    
def get_revenue():
#revenue sheet
    set_dir()
    worksheet_revenue = pd.read_csv('Revenue_sheet.csv', header=None)
    revenuerows = worksheet_revenue[1:]
    return revenuerows

def fetch_budgets():
    set_dir()
    budget_expenses = pd.read_csv('budget_expenses.csv')
    budget_revenues = pd.read_csv('budget_revenue.csv')
    return budget_expenses, budget_revenues

#fetches totals and counts of each catgory in the files
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

#returns the total and count of a specific month
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

#returns the total of unnecesary and restrant transactions only
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
    set_dir()