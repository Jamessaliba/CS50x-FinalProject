from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout,
    QComboBox, QTableWidget, QHeaderView, QPushButton,QDateEdit, QDoubleSpinBox, QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox)

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIcon
import os
import pandas as pd
import Spreadsheet_operator as sheet

class WorksheetDialog(QDialog):
    def __init__(self, worksheets, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        label = QLabel("Select the worksheet for this entry:")
        layout.addWidget(label)

        self.worksheet_box = QComboBox()
        self.worksheet_box.addItems(worksheets)
        layout.addWidget(self.worksheet_box)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)

    def selected_worksheet(self):
        return self.worksheet_box.currentText()
    
class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
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
                                     "Gifts", "Shopping", "Super Contributions", "Donations", "For home", "For others", "Alone,", "With Others", 
                                     "Subscriptions", "Income", "Wage", "interest", "Capital Gains", "Shares", "Contributions", "Refund", "Termination Payment", "Other"]
        self.worksheets_name = ["Expenses", "Revenue"]
        self.taxable = ["FALSE","TRUE"]
        self.row_worksheets = {}

        self.print_button = QPushButton('Save')
        self.print_button.pressed.connect(self.save_content)

        self.add_row = QPushButton("add row")
        self.add_row.pressed.connect(self.select_worksheet)

        layout = QGridLayout()
        layout.addWidget(self.table, 0,0)
        layout.addWidget(self.print_button,1,0)
        layout.addWidget(self.add_row)

        self.setLayout(layout)

    def select_worksheet(self):
        """Ask the user which worksheet the new row belongs to."""

        dialog = WorksheetDialog(self.worksheets_name, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            worksheet_name = dialog.selected_worksheet()
            self.increase_rows(worksheet_name)

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