from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout, QCompleter
from PyQt6.QtCore import QDate, Qt
import pandas as pd
import Spreadsheet_operator as sheets

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Bar with Suggestions")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        layout.addWidget(self.search_bar)
        expenses = sheets.get_expense()
        entities = set()
        for index, item in expenses.iterrows():
            entities.add(item[1])
        
        completer = QCompleter(entities)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_bar.setCompleter(completer)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())