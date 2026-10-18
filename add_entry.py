from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout,
    QComboBox, QTableWidget, QHeaderView, QPushButton,QDateEdit, QDoubleSpinBox, QLineEdit,
      QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QCompleter)

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import os
import pandas as pd
import Spreadsheet_operator as sheet
import report_page 
import statistics_page
import view_entrys
    
class ReportWindow(QWidget):
    data_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        #background data
        self.setWindowTitle("Accounting Add entry")
        self.table = QTableWidget(0, 9)
        self.expenses = sheet.get_expense()
        self.revenues = sheet.get_revenue()
        self.expenses_codes = self.make_code_lib(self.expenses)
        self.revenues_codes = self.make_code_lib(self.revenues)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setHorizontalHeaderLabels(["Worksheet","entity", "amount", "category","sub-category", "date", "Transaction","tax", ""])
        self.expense_categories = ['Necessary','Groceries', 'Unnecessary','Restaurant','Temporary']
        self.revenue_categories = ['Income','Contributions']
        self.sub_categories = ["", "Business", "Bills/utilities", "Education", "Medical", "Insurence", "Transport", "Entertainment", 
                                     "Gifts", "Shopping", "Super Contributions", "Donations", "For home", "For others", "Alone", "With Others", 
                                     "Subscriptions", "Income", "Wage", "interest", "Capital Gains", "Shares", "Contributions", "Refund", "Termination Payment", "Other"]
        self.sub_categories.sort()
        self.worksheets_name = ["Expenses", "Revenue"]
        self.taxable = ["FALSE","TRUE"]
        self.row_worksheets = {} #used for delete function
        entity_search = set()
        for index, item in self.expenses.iterrows():
            entity_search.add(item[1])
        for index, item in self.revenues.iterrows():
            entity_search.add(item[1])
        self.completer = QCompleter(entity_search)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        

        #layout
        self.save_button = QPushButton('Save')
        self.save_button.pressed.connect(self.save_content)

        self.add_expense_button = QPushButton("Expenses")
        self.add_expense_button.setIcon(QIcon("green_plus.png"))
        self.add_expense_button.pressed.connect(lambda: self.select_worksheet(self.add_expense_button.text()))
        self.add_expense_button.setFixedSize(200,25)
        self.add_revenue_button = QPushButton("Revenue")
        self.add_revenue_button.setIcon(QIcon("green_plus.png"))
        self.add_revenue_button.pressed.connect(lambda: self.select_worksheet(self.add_revenue_button.text()))
        self.add_revenue_button.setFixedSize(200,25)

        add_entry_layout = QHBoxLayout()
        add_entry_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        add_entry_layout.addWidget(self.add_expense_button)
        add_entry_layout.addWidget(self.add_revenue_button)
        container = QVBoxLayout()
        container.addLayout(add_entry_layout)
        container.addWidget(self.table)
        container.addWidget(self.save_button)

        self.setLayout(container)

    def select_worksheet(self, button):
        self.increase_rows(button)

    def save_content(self):
        for row in range(self.table.rowCount()):
            worksheet_tab = self.row_worksheets[row]
            entity = self.table.cellWidget(row, 1).text()
            amount = self.table.cellWidget(row, 2).value()
            category = self.table.cellWidget(row, 3).currentText()
            sub_catagory = self.table.cellWidget(row, 4).currentText()
            date = self.table.cellWidget(row, 5).date().toString("dd/MM/yyyy")
            description = self.table.cellWidget(row, 6).text()
            tax_tab = self.table.cellWidget(row, 7).currentText()

            if worksheet_tab == "Expenses":
                code = self.make_code(self.expenses_codes, category)
            else:
                code = self.make_code(self.revenues_codes, category)
            data = {"code":[code],
                    "entity":[entity],
                    "amount":[amount],
                    "category":[category],
                    "sub-category":[sub_catagory],
                    "transaction":[description],
                    "date":[date],
                    "taxable": [tax_tab]}

            #save file
            df = pd.DataFrame(data)
            if worksheet_tab == 'Expenses':
                df.to_csv('Expenses_sheet.csv', mode='a', index=False, header=False)
            else:
                df.to_csv('Revenue_sheet.csv', mode='a', index=False, header=False)

        #remove all rows from the table after saving
        for row in range(self.table.rowCount()):
            self.table.removeRow(row)
        self.table.setRowCount(0)

        self.data_saved.emit()


    def increase_rows(self, worksheet_name):
        row = self.table.rowCount()

        self.table.insertRow(row)

        self.row_worksheets[row] = worksheet_name

            #worksheet
        worksheet_tab = QLabel(worksheet_name)
        self.table.setCellWidget(row, 0, worksheet_tab)
            # entity
        entity = QLineEdit()
        entity.setPlaceholderText("Enter Entity...")
        entity.setCompleter(self.completer)
        self.table.setCellWidget(row, 1, entity)

            # Amount
        amount = QDoubleSpinBox()
        amount.setMaximum(1000000)
        amount.setPrefix("$")
        amount.setDecimals(2)
        self.table.setCellWidget(row, 2, amount)

            # Category combo
        category = QComboBox()

        if worksheet_name == "Expenses":
            category.addItems(self.expense_categories)
        elif worksheet_name == "Revenue":
            category.addItems(self.revenue_categories)

        self.table.setCellWidget(row, 3, category)

            #sub-category
        sub_category = QComboBox()
        sub_category.addItems(self.sub_categories)
        self.table.setCellWidget(row, 4, sub_category)


            # date
        date = QDateEdit()
        date.setCalendarPopup(True)
        date.setDate(QDate.currentDate())
        self.table.setCellWidget(row, 5, date)

            # Description
        description = QLineEdit()
        description.setPlaceholderText("Enter description...")
        self.table.setCellWidget(row, 6, description)

            # Tax Tab
        TaxTab = QComboBox()
        TaxTab.addItems(self.taxable)
        self.table.setCellWidget(row, 7, TaxTab)

            # Delete button
        delete_button = QPushButton(icon=QIcon("red_cross.png"), text="")
        delete_button.setFixedSize(40, 25)
        delete_button.clicked.connect(lambda checked=False, row=row: self.delete_row(row))
        button_centreing = QHBoxLayout()
        button_centreing.addWidget(delete_button)
        button_centreing.setAlignment(delete_button, Qt.AlignmentFlag.AlignCenter)
        button_centreing.setContentsMargins(0,0,0,1)
        
        self.table.setCellWidget(row, 8, QWidget())
        self.table.cellWidget(row, 8).setLayout(button_centreing)

    def delete_row(self, row):
        if row < 0 or row >= self.table.rowCount():
            return

        # Remove the row from the table.
        self.table.removeRow(row)

        # Rebuild the worksheet dictionary
        new_row_worksheets = {}

        for current_row in range(self.table.rowCount()):
            if current_row < row:
                new_row_worksheets[current_row] = self.row_worksheets[current_row]
            else:
                new_row_worksheets[current_row] = self.row_worksheets[current_row + 1]

        self.row_worksheets = new_row_worksheets

    def make_code(self, data, category):
        highest = 0
        for cell in data:
            if category[0:3].upper() == cell[0:3]:
                try:
                    num = int(cell[4:])
                except ValueError:
                    continue
                if num > highest:
                    highest = num
        new_code = category[0:3].upper() + str(highest + 1).zfill(4)
        data.append(new_code)
        return new_code

    def make_code_lib(self, data):
        lib =[]
        for index, row in data.iterrows():
            lib.append(row[0])
        return lib

    def update_categories(self, worksheet, category_box):
        category_box.clear()

        if worksheet == "Expenses":
            category_box.addItems(self.expense_categories)

        elif worksheet == "Revenue":
            category_box.addItems(self.revenue_categories)

if __name__ == "__main__":
    app = QApplication([])
    window = ReportWindow()
    window.resize(975,700)
    window.show()
    app.exec()