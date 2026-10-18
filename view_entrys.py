from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,QDateEdit, QLineEdit,
      QVBoxLayout, QHBoxLayout
)

from PyQt6.QtCore import QDate, Qt
import os
import Spreadsheet_operator as sheet

class ViewEntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #set up layouts
        contanier = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        filter_layout = QHBoxLayout()
        filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contanier.addLayout(button_layout)
        contanier.addLayout(filter_layout)

        #set up status bar
        self.status_bar = self.statusBar()
        self.total_amount = QLabel()
        self.cell_count = QLabel()
        self.status_bar.addPermanentWidget(self.total_amount)
        self.status_bar.addPermanentWidget(self.cell_count)

        #set up catagories/subcatagories
        self.catagorys = ["All Catagories", "Necessary", "Groceries", "Unnecessary", "Restaurant", "Temporary", "Income", "Contributions"]
        self.subcatagorys = ["All Sub-subcatagories", "Business", "Bills/utilities", "Education", "Medical", "Insurence", "Transport", "Entertainment", 
                             "Gifts", "Shopping", "Super Contributions", "Donations", "For home", "For others", "Alone,", "With Others", 
                             "Subscriptions", "Income", "Wage", "interest", "Capital Gains", "Shares", "Contributions", "Refund", "Termination Payment", "Other"]
        self.subcatagorys.sort()
        self.toggle = True
        self.get_data()

        #set up expense, revenue and search buttons
        expense_button = QPushButton("Expenses")
        expense_button.setFixedSize(200,25)
        expense_button.pressed.connect(lambda: self.toggle_data(expense_button.text()))
        expense_button.pressed.connect(self.search_entries)
        revenue_button = QPushButton("Revenue")
        revenue_button.setFixedSize(200,25)
        revenue_button.pressed.connect(lambda: self.toggle_data(revenue_button.text()))
        revenue_button.pressed.connect(self.search_entries)
        search_button = QPushButton("Search")
        search_button.setFixedSize(200,25)
        search_button.clicked.connect(self.search_entries)
        button_layout.addWidget(expense_button)
        button_layout.addWidget(revenue_button)
        button_layout.addWidget(search_button)

        #search bar and filters
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search through entities and descriptions...")
        self.search_bar.setFixedSize(200,25)
        filter_layout.addWidget(self.search_bar)

        self.category_filter = QComboBox()
        self.category_filter.setFixedSize(200,25)
        self.category_filter.addItems(self.catagorys)
        filter_layout.addWidget(self.category_filter)

        self.subcategory_filter = QComboBox()
        self.subcategory_filter.setFixedSize(200,25)
        self.subcategory_filter.addItems(self.subcatagorys)
        filter_layout.addWidget(self.subcategory_filter)

        self.month_filter_lower = QDateEdit()
        self.month_filter_lower.setCalendarPopup(True)
        self.month_filter_lower.setDate(QDate.currentDate().addDays(-7))  # Set to one month ago
        self.month_filter_upper = QDateEdit()
        self.month_filter_upper.setCalendarPopup(True)
        self.month_filter_upper.setDate(QDate.currentDate())  # Set to today
        filter_layout.addWidget(self.month_filter_lower)
        filter_layout.addWidget(self.month_filter_upper)

        self.setWindowTitle("Accounting Add entry")
        self.table_entries = QTableWidget(0, 8)
        self.table_entries.setHorizontalHeaderLabels(["Code", "Entity", "Amount", "Category","Sub-catagory", "Transaction", "Date", "taxable"])
        self.table_entries.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.search_entries()  # Populate the table with initial data
        contanier.addWidget(self.table_entries)

        widget = QWidget()
        widget.setLayout(contanier)
        self.setCentralWidget(widget)

    #toggle between data sets
    def toggle_data(self, button):
        print(button)
        if button == "Expenses":
            self.toggle = True
        else:
            self.toggle = False


    def get_data(self):
        self.expenses = sheet.get_expense()
        self.revenues = sheet.get_revenue()

    def search_entries(self):
        array = []
        amount = 0
        count = 0
        keywords = self.search_bar.text().lower().split()
        if self.category_filter.currentText() == "All Catagories": 
            catagory = "" 
        else:
            catagory = self.category_filter.currentText()
        if self.subcategory_filter.currentText() == "All Sub-subcatagories":
            subcatagory = ""
        else:
            subcatagory = self.subcategory_filter.currentText()
        earlier_date = self.month_filter_lower.date().toPyDate()
        later_date = self.month_filter_upper.date().toPyDate()
        if self.toggle == True:
            data = self.expenses
        else:
            data = self.revenues
        for index, row in data.iterrows():
            day, month, year = str(row[6]).split('/')
            entry_date = QDate(int(year), int(month), int(day)).toPyDate()
            if all(keyword in str(row).lower() for keyword in keywords) and \
               (catagory == "" or row[3] == catagory) and \
               (subcatagory == "" or row[4] == subcatagory) and \
               (earlier_date <= entry_date <= later_date):
                array.append(row)
                count += 1
                amount += float(row[2].replace('$', '').replace(',', ''))
        self.table_entries.setRowCount(0)  # Clear the table
        for row in array:
            self.table_entries.insertRow(self.table_entries.rowCount())
            for col, value in enumerate(row):
                self.table_entries.setItem(self.table_entries.rowCount() - 1, col, QTableWidgetItem(str(value)))
        self.total_amount.setText(f"Total amount {str(amount)}")
        self.cell_count.setText(f"Cells: {str(count)}")



if __name__ == "__main__":
    app = QApplication([])
    window = ViewEntryWindow()
    window.resize(975,700)
    window.show()
    app.exec()