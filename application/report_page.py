
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
import Spreadsheet_operator as sheet_data
from datetime import datetime

class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()

        #gather data
        self.expense_data = sheet_data.get_expense()
        self.revenue_data = sheet_data.get_revenue()
        self.current_month = datetime.now().strftime("%m")

        #set up month dropbox
        months_to_date = [f"{i:02d}" for i in range(1, int(self.current_month) + 1)]
        self.month = QComboBox()
        self.month.addItems(months_to_date)
        self.month.setCurrentText(self.current_month)

        #set up tables
        self.expense_table = QTableWidget()
        self.revenue_table = QTableWidget()
        self.totals_table = QTableWidget()
        self.totals_table.setColumnCount(3)
        self.totals_table.setHorizontalHeaderLabels(["Total expenses", "Total revenue", "net profit/loss"])
        self.totals_table.verticalHeader().hide()
        self.totals_table.setAlternatingRowColors(True)
        self.totals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.totals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.create_tables()

        #set up layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Month"),0,0)
        layout.addWidget(self.month,0,1)
        layout.addWidget(QLabel("Expenses"),1,0)
        layout.addWidget(self.expense_table,2,0,1,4)
        layout.addWidget(QLabel("Revenue"),3,0)
        layout.addWidget(self.revenue_table,4,0,1,4)
        layout.addWidget(QLabel("Totals"),5,0)
        layout.addWidget(self.totals_table, 6,0,1,3)

        self.setLayout(layout)

        self.month.currentTextChanged.connect(self.update_report)
        self.update_report(self.month.currentText())

    def create_tables(self):
        for table in (self.expense_table, self.revenue_table):
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(
                ["Category","Amount","Transactions","Average"]
            )
            table.verticalHeader().hide()
            table.setAlternatingRowColors(True)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch
            )
            
    def get_data(self):
        self.expense_data = sheet_data.get_expense()
        self.revenue_data = sheet_data.get_revenue()
        self.update_report(self.month.currentText())

    def update_report(self, month):
        self.populate_expense_table(month)
        self.populate_revenue_table(month)
        self.populate_totals_table(month)

    def populate_expense_table(self, month):
        totals, counts = sheet_data.cata_totals_count(self.expense_data, month)
        categories = ["Necessary","Groceries", "Unnecessary", "Restaurant", "Temporary"]
        self.expense_table.setRowCount(len(categories))
        for category in categories:
            total = totals.get(category, 0)
            count = counts.get(category + " count", 0)
            average = total / count if count else 0
            row = categories.index(category)
            self.expense_table.setItem(row,0,QTableWidgetItem(category))
            self.expense_table.setItem(row,1,QTableWidgetItem(f"${total:,.2f}"))
            self.expense_table.setItem(row,2,QTableWidgetItem(str(count)))
            self.expense_table.setItem(row,3,QTableWidgetItem(f"${average:,.2f}"))

    def populate_revenue_table(self, month):
        totals, counts = sheet_data.cata_totals_count(self.revenue_data, month)
        categories = ["Income", "Contributions"]
        self.revenue_table.setRowCount(len(categories))
        for category in categories:
            total = totals.get(category, 0)
            count = counts.get(category + " count", 0)
            average = total / count if count else 0
            row = categories.index(category)
            self.revenue_table.setItem(row,0,QTableWidgetItem(category))
            self.revenue_table.setItem(row,1,QTableWidgetItem(f"${total:,.2f}"))
            self.revenue_table.setItem(row,2,QTableWidgetItem(str(count)))
            self.revenue_table.setItem(row,3,QTableWidgetItem(f"${average:,.2f}"))
    
    def populate_totals_table(self, month):
        expenses_totals, expense_counts = sheet_data.cata_totals_count(self.expense_data, month)
        total_expenses = 0
        for item in expenses_totals:
            total_expenses += expenses_totals[item]

        revenue_totals, revenue_counts = sheet_data.cata_totals_count(self.revenue_data, month)
        total_revenue = 0
        for item in revenue_totals:
            total_revenue += revenue_totals[item]

        self.totals_table.setRowCount(1)
        self.totals_table.setItem(0,0,QTableWidgetItem(f"{total_expenses:,.2f}"))
        self.totals_table.setItem(0,1,QTableWidgetItem(f"{total_revenue:,.2f}"))
        self.totals_table.setItem(0,2,QTableWidgetItem(f"{total_revenue - total_expenses:,.2f}"))

if __name__ == "__main__":
    app = QApplication([])
    window = ReportWindow()
    window.resize(975,700)
    window.show()
    app.exec()
