from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,QDateEdit, QDoubleSpinBox, QLineEdit,
      QVBoxLayout, QDialog, QDialogButtonBox, QHBoxLayout,
)
import calendar
import datetime
from pathlib import Path
import os
import pandas as pd
from PyQt6.QtCore import QSize, Qt, QDate
from PyQt6.QtGui import QIcon
import Spreadsheet_operator as sheet
import Icon_operator as icon


class BudgetWindow(QWidget):
    def __init__(self):
        super().__init__()
        contanier = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        self.expense_df, self.revenue_df = sheet.fetch_budgets()

        # left side entry layout
        self.budget_table = QTableWidget(8, 2)
        self.budget_table.verticalHeader().setVisible(False)
        self.budget_table.setHorizontalHeaderLabels(["monthly budget:", ""])
        self.budget_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.budget_table.setItem(0, 0, QTableWidgetItem("net monthly allowance:"))
        self.budget_table.setItem(1, 0, QTableWidgetItem("max daily spending:"))
        self.budget_table.setItem(2, 0, QTableWidgetItem("spent so far:"))
        self.budget_table.setItem(3, 0, QTableWidgetItem("remaining days (including today):"))
        self.budget_table.setItem(4, 0, QTableWidgetItem("number of days this month:"))
        self.budget_table.setItem(5, 0, QTableWidgetItem("remaining allowance:"))
        self.budget_table.setItem(6, 0, QTableWidgetItem("actually allowed daily spending:"))
        self.budget_table.setItem(7, 0, QTableWidgetItem("current rate of spending per day:"))
        update_budget_button = QPushButton("Update Budget")
        update_budget_button.pressed.connect(self.update_page)
        # few couple of days recommended spending

        self.calander_budget_table = QTableWidget(3,3)
        self.calander_budget_table.verticalHeader().setVisible(False)
        self.calander_budget_table.setHorizontalHeaderLabels(["Date", "Amount", "difference"])
        self.calander_budget_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout1.addWidget(self.budget_table)
        layout1.addWidget(update_budget_button)
        layout1.addWidget(self.calander_budget_table)

        # right side entry layout
        # expenses
        expense_label = QLabel("Expenses")
        self.expenses_table = QTableWidget(len(self.expense_df), 3)
        self.expenses_table.setHorizontalHeaderLabels(["Item", "Amount", ""])
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.add_expense_button = QPushButton("add expense")
        self.add_expense_button.setIcon(QIcon(icon.get_icon("green_plus.png")))
        self.add_expense_button.pressed.connect(lambda: self.add_row("expense"))

        #revenues
        revenue_label = QLabel("Revenues")
        self.revenues_table = QTableWidget(len(self.revenue_df), 3)
        self.revenues_table.setHorizontalHeaderLabels(["Item", "Amount", ""])
        self.revenues_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.add_revenue_button = QPushButton("add revenues")
        self.add_revenue_button.setIcon(QIcon(icon.get_icon("green_plus.png")))
        self.add_revenue_button.pressed.connect(lambda: self.add_row("revenue"))

        layout2.addWidget(expense_label)
        layout2.addWidget(self.expenses_table)
        layout2.addWidget(self.add_expense_button)
        layout2.addWidget(revenue_label)
        layout2.addWidget(self.revenues_table)
        layout2.addWidget(self.add_revenue_button)

        self.update_budget_table()
        self.generate_right_table()
        self.update_calander_table()

        # Add the two main sections to the horizontal container
        contanier.addLayout(layout1, 1)
        contanier.addLayout(layout2, 1)
        self.setLayout(contanier)

    def update_page(self):
        self.update_files()
        self.update_budget_table()
        self.generate_right_table()
        self.update_calander_table()

    def update_budget_table(self):
        self.total_expenses = self.expense_df['amount'].sum()
        self.total_revenue = self.revenue_df['amount'].sum()
        self.monthly_allowence = self.total_revenue - self.total_expenses
        current_date = datetime.date.today()
        today = str(current_date).split('-')[2]
        _, num_days_in_month = calendar.monthrange(current_date.year, current_date.month)
        self.spent_this_month = sheet.spent_month('09')
        remaining_days = int(num_days_in_month) - int(today) +1
        try:
            daily_spending = (self.monthly_allowence - self.spent_this_month)/remaining_days
        except ZeroDivisionError:
            daily_spending = self.monthly_allowence - self.spent_this_month
        self.budget_table.setItem(0, 1, QTableWidgetItem(f"{self.monthly_allowence:,.2f}"))
        self.budget_table.setItem(1, 1, QTableWidgetItem(f"{self.monthly_allowence/30.4:,.2f}"))
        self.budget_table.setItem(2, 1, QTableWidgetItem(f"{self.spent_this_month:,.2f}"))
        self.budget_table.setItem(3, 1, QTableWidgetItem(f"{remaining_days}"))
        self.budget_table.setItem(4, 1, QTableWidgetItem(f"{num_days_in_month}"))
        self.budget_table.setItem(5, 1, QTableWidgetItem(f"{self.monthly_allowence - self.spent_this_month:,.2f}"))
        self.budget_table.setItem(6, 1, QTableWidgetItem(f"{daily_spending:,.2f}"))
        self.budget_table.setItem(7, 1, QTableWidgetItem(f"{self.spent_this_month/(int(today)):.2f}"))

    def update_calander_table(self):
        self.calander_budget_table.setRowCount(0)  # Clear existing rows
        current_date = datetime.date.today()
        _, num_days_in_month = calendar.monthrange(current_date.year, current_date.month)
        calander_array = []
        for day in range(1, num_days_in_month + 1):
            date = day
            amount = (self.monthly_allowence - self.spent_this_month) / (num_days_in_month - day + 1)
            if day == num_days_in_month:
                difference = 0
            else:
                difference = abs((self.monthly_allowence - self.spent_this_month) / (num_days_in_month - day)
                                -(self.monthly_allowence - self.spent_this_month) / (num_days_in_month - day + 1))
            calander_array.append((date, amount, f"{difference:,.2f}"))

        for item in range(len(calander_array)):
            self.calander_budget_table.insertRow(item)
            self.calander_budget_table.setItem(item, 0, QTableWidgetItem(str(calander_array[item][0])))
            self.calander_budget_table.setItem(item, 1, QTableWidgetItem(f"{calander_array[item][1]:,.2f}"))
            self.calander_budget_table.setItem(item, 2, QTableWidgetItem(calander_array[item][2]))
  
    def update_files(self):
        # Update the expense DataFrame with the current data from the expenses_table
        self.expense_df = pd.DataFrame(columns=["item", "amount"])
        for row in range(self.expenses_table.rowCount()):
            item = self.expenses_table.item(row, 0)
            amount = self.expenses_table.item(row, 1)
            if item is not None and amount is not None:
                try:
                    float_amount = float(amount.text())
                except ValueError:
                    continue #create message box to inform user of invalid input
                self.expense_df = pd.concat([self.expense_df, pd.DataFrame({"item": [item.text()], "amount": [float_amount]})], ignore_index=True)

        # Update the revenue DataFrame with the current data from the revenues_table
        self.revenue_df = pd.DataFrame(columns=["item", "amount"])
        for row in range(self.revenues_table.rowCount()):
            item = self.revenues_table.item(row, 0)
            amount = self.revenues_table.item(row, 1)
            if item is not None and amount is not None:
                try:
                    float_amount = float(amount.text())
                except ValueError:
                    continue #create message box to inform user of invalid input
                self.revenue_df = pd.concat([self.revenue_df, pd.DataFrame({"item": [item.text()], "amount": [float_amount]})], ignore_index=True)

        # Save the updated DataFrames to CSV files
        current_directory = Path(__file__).resolve().parent
        project_directory = current_directory.parent
        csv_directory = project_directory / "CSV_files"

        self.expense_df.to_csv(os.path.join(csv_directory,'budget_expenses.csv'), index=False)
        self.revenue_df.to_csv(os.path.join(csv_directory,'budget_revenue.csv'), index=False)

    def generate_right_table(self):
        #expenses
        self.expenses_table.setRowCount(len(self.expense_df))
        for i, row in self.expense_df.iterrows():
            self.expenses_table.setItem(i, 0, QTableWidgetItem(str(row["item"])))
            self.expenses_table.setItem(i, 1, QTableWidgetItem(str(row["amount"])))
            self.expenses_table.setCellWidget(i, 2, self.create_centered_delete_button())

        # Revenues
        self.revenues_table.setRowCount(len(self.revenue_df))
        for i, row in self.revenue_df.iterrows():
            self.revenues_table.setItem(i, 0, QTableWidgetItem(str(row["item"])))
            self.revenues_table.setItem(i, 1, QTableWidgetItem(str(row["amount"])))
            self.revenues_table.setCellWidget(i, 2, self.create_centered_delete_button())


    def add_row(self, worksheet):
        if worksheet == "expense":
            table = self.expenses_table
        elif worksheet == "revenue":
            table = self.revenues_table
        else:
            return

        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setCellWidget(row_position, 2, self.create_centered_delete_button())

    def delete_row(self):
        button = self.sender()
        if button is None:
            return

        for table in [self.expenses_table, self.revenues_table]:
            for row in range(table.rowCount()):
                container = table.cellWidget(row, 2)

                if container is not None and button in container.findChildren(QPushButton):
                    table.removeRow(row)
                    return

    def create_delete_button(self):
        delete_button = QPushButton()
        delete_button.setIcon(QIcon(icon.get_icon("red_cross.png")))
        delete_button.setIconSize(QSize(16, 16))
        delete_button.setFixedSize(40, 25)
        delete_button.setToolTip("Delete row")
        delete_button.clicked.connect(self.delete_row)
        return delete_button

    def create_centered_delete_button(self):
        container = QWidget()
        layout = QHBoxLayout(container)

        layout.addWidget(self.create_delete_button())
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 1)

        return container

if __name__ == "__main__":
    app = QApplication([])
    window = BudgetWindow()
    window.resize(975,700)
    window.show()
    app.exec()