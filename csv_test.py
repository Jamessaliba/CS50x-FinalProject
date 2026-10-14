import csv
import pandas as pd

toggle = input("enter input ('r' for read, 'w' for write, 'd' for delete): ")  # Set to 'r' to read the CSV file, 'w' to write to it
# Open CSV file
#note: only seems to work with empty line at the bottom

if toggle == 'r':
    df = pd.read_csv('budget_expenses.csv')
    print(df)

if toggle == 'w':
    # Open the CSV file in append mode
    new_data = {'item': 'subscription', 'amount': '80'}
    w = pd.DataFrame([['subscription', '80']], columns=['item', 'amount'])
    w.to_csv('budget_expenses.csv', mode='a', index=False, header=False)

if toggle == 'd':
    # Step 1: Read the CSV file
    df = pd.read_csv('budget_expenses.csv')

    # Step 2: Drop(delete) the last row
    df = df.drop(df.index[-1])

    # Step 3: Save the changes back to the CSV file
    df.to_csv('budget_expenses.csv', index=False)

if toggle == 'c':
    df = pd.read_csv('budget_expenses.csv')
    print(len(df))