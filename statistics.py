from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QLabel, QGridLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
import Spreadsheet_operator as sheet_data

class statisticsPage(QWidget):
    def __init__(self):
        super().__init__()
        toplayout = QHBoxLayout()
        bottomlayout = QHBoxLayout()

        self.expense_data = sheet_data.get_expense()
        self.revenue_data = sheet_data.get_revenue()
        self.monthly_expenses = MonthlyExpenses()
        self.totals_amounts = calculate_totals()
        self.spending_per_day = SpentThisMonth()
        self.netratio = netratio()

        self.monthly_expenses.update_bar_chart_EXP(self.expense_data)
        self.totals_amounts.update_bar_chart_totals(self.expense_data, self.revenue_data)
        self.spending_per_day.update_spending_this_month(self.expense_data)
        self.netratio.update_Piechart(self.expense_data, datetime.now().strftime("%m"))

        toplayout.addWidget(self.monthly_expenses)
        toplayout.addWidget(self.totals_amounts)
        bottomlayout.addWidget(self.spending_per_day)
        bottomlayout.addWidget(self.netratio)
        layout = QVBoxLayout()
        layout.addLayout(toplayout)
        layout.addLayout(bottomlayout)
        self.setLayout(layout)

class MonthlyExpenses(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)

    def update_bar_chart_EXP(self, expense_data):

        self.axes.clear()
        total_expenses = {}
        for index, expense in expense_data.iterrows():
            day, month, year = expense[6].split('/')
            total_expenses[month] = total_expenses.get(month, 0) + float(expense[2].replace('$', '').replace(',', ''))

        calander_months = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
        months = []
        expenses = []
        for month, expense in total_expenses.items():
            if month < datetime.now().strftime("%m"):
                months.append(calander_months[month])
                expenses.append(expense)

        x = np.polyfit(range(len(months)), expenses, 1)
        self.axes.plot(np.arange(len(months)), np.polyval(x, np.arange(len(months))), color='blue', linestyle='--', label='Trend Line')
        self.axes.plot(months, expenses, color='red', label='Expenses')
        self.axes.set_title("Monthly Expenses")
        self.axes.set_ylabel("$")

        self.draw()

class calculate_totals(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)

    def update_bar_chart_totals(self, expense_data, revenue_data):

        self.axes.clear()
        total_expenses = 0
        total_revenues = 0
        for index, expense in expense_data.iterrows():
            total_expenses += float(expense[2].replace('$', '').replace(',', ''))
        for index, revenue in revenue_data.iterrows():
            total_revenues += float(revenue[2].replace('$', '').replace(',', ''))

        self.axes.bar(['Expenses', 'Revenues'], [total_expenses, total_revenues], color=['red', 'green'], label=['Expenses', 'Revenues'])
        self.axes.set_title("Total Expenses vs Revenues")
        self.axes.set_ylabel("$")

        self.draw()

class SpentThisMonth(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)
    def update_spending_this_month(self, expense_data):

        self.axes.clear()
        total_spent_per_day = {}
        current_month = datetime.now().month
        for index, expense in expense_data.iterrows():
            day, month, year = expense[6].split('/')
            if int(month) == current_month:
                total_spent_per_day[day] = total_spent_per_day.get(day, 0) + float(expense[2].replace('$', '').replace(',', ''))

        days = list(total_spent_per_day.keys())
        amounts = list(total_spent_per_day.values())

        self.axes.plot(days, amounts, color='blue', label='Expenses')
        self.axes.set_title("Spending This Month")
        self.axes.set_ylabel("$")

        self.draw()

class netratio(FigureCanvasQTAgg):
    def __init__(self):
        #this is consistant
        fig = Figure(figsize=(4, 3))
        self.axes = fig.add_subplot(111)
        
        super().__init__(fig)
        
    def update_Piechart(self, expense_data, month):

        # Remove the old chart
        self.axes.clear()

        # Get the filtered data
        totals, counts = sheet_data.cata_totals_count(expense_data, month)

        categories = []
        amounts = []

        for category, amount in totals.items():
            categories.append(category)
            amounts.append(amount)

        # Draw the new chart
        self.axes.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )
        self.draw()



if __name__ == "__main__":
    app = QApplication([])
    window = statisticsPage()
    window.resize(975,700)
    window.show()
    app.exec()
