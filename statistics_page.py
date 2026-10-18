from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QWidget,
    QComboBox,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
import Spreadsheet_operator as sheet_data

class statisticsPage(QWidget):
    def __init__(self):
        super().__init__()
        #set up layouts
        controls_layout =QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        #set up month drop box
        self.current_month = datetime.now().strftime("%m")
        months_to_date = [f"{i:02d}" for i in range(1, int(self.current_month) + 1)]
        self.month = QComboBox()
        self.month.addItems(months_to_date)
        self.month.setFixedSize(200,25)
        self.month.setCurrentText(self.current_month)

        #set up graphs
        self.monthly_expenses = MonthlyExpenses()
        self.totals_amounts = calculate_totals()
        self.spending_per_day = SpentThisMonth()
        self.netratio = netratio()
        self.month_totals = calculate_month_totals()

        #populate graphs
        self.get_data()

        controls_layout.addWidget(self.month)
        top_layout.addWidget(self.netratio)
        top_layout.addWidget(self.spending_per_day)
        top_layout.addWidget(self.month_totals)

        bottom_layout.addWidget(self.totals_amounts)
        bottom_layout.addWidget(self.monthly_expenses)

        layout = QVBoxLayout()
        layout.addLayout(controls_layout)
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

        #signals
        self.month.currentTextChanged.connect(self.update_tables)

    def get_data(self):
        self.expense_data = sheet_data.get_expense()
        self.revenue_data = sheet_data.get_revenue()
        self.update_tables()

    def update_tables(self):
        self.monthly_expenses.update_plot_chart_EXP(self.expense_data)
        self.totals_amounts.update_bar_chart_totals(self.expense_data, self.revenue_data)
        self.spending_per_day.update_spending_this_month(self.expense_data, self.month.currentText())
        self.netratio.update_Piechart(self.expense_data, self.month.currentText())
        self.month_totals.update_bar_chart_month_totals(self.expense_data,self.revenue_data,self.month.currentText())

#Totals expenses graph for the year with data up to the previous month
class MonthlyExpenses(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)

    def update_plot_chart_EXP(self, expense_data):

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

#total expenses and revenue up to today
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

        bars = self.axes.bar(['Expenses', 'Revenues'], [total_expenses, total_revenues], color=['red', 'green'], label=['Expenses', 'Revenues'])
        self.axes.bar_label(bars, padding=3)
        self.axes.set_ylim(0, max([total_expenses, total_revenues]) * 1.1)
        self.axes.set_title("Total Expenses vs Revenues")
        self.axes.set_ylabel("$")

        self.draw()

#totals of the selected months total expenses and revenues
class calculate_month_totals(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)

    def update_bar_chart_month_totals(self, expense_data, revenue_data, current_month):

        self.axes.clear()
        total_expenses = 0
        total_revenues = 0
        for index, expense in expense_data.iterrows():
            day, month, year = expense[6].split('/')
            if int(month) == int(current_month):
                total_expenses += float(expense[2].replace('$', '').replace(',', ''))

        for index, revenue in revenue_data.iterrows():
            day, month, year = revenue[6].split('/')
            if int(month) == int(current_month):
                total_revenues += float(revenue[2].replace('$', '').replace(',', ''))

        bars = self.axes.bar(['Expenses', 'Revenues'], [total_expenses, total_revenues], color=['red', 'green'], label=['Expenses', 'Revenues'])
        self.axes.bar_label(bars, padding=3)
        self.axes.set_ylim(0, max([total_expenses, total_revenues]) * 1.1)
        self.axes.set_title("Total Expenses vs Revenues")
        self.axes.set_ylabel("$")

        self.draw()

#line graph of spending each day of selected month
class SpentThisMonth(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.axes = fig.add_subplot(111)

        super().__init__(fig)
    def update_spending_this_month(self, expense_data, current_month):

        self.axes.clear()
        total_spent_per_day = {}
        for index, expense in expense_data.iterrows():
            day, month, year = expense[6].split('/')
            if int(month) == int(current_month):
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
        self.axes.set_title("Category Ratio")
        self.draw()



if __name__ == "__main__":
    app = QApplication([])
    window = statisticsPage()
    window.resize(975,700)
    window.show()
    app.exec()
