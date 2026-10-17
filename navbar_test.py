from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QLabel)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from report_page import ReportWindow
from add_entry import ReportWindow as AddEntryReportWindow
from budgetor import BudgetWindow
from view_entrys import ViewEntryWindow
from statistics_page import statisticsPage

class loader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("loader")
        self.label_loading = QLabel("Loading...")
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(self.label_loading)
        self.setCentralWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Accounting App")

        pagelayout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(self.stacklayout)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        #loader
        loading = loader()
        self.stacklayout.addWidget(loading)

        # Overview
        button1 = QAction("overview", self)
        button1.triggered.connect(self.activate_tab_1)

        overview_page = ReportWindow()
        self.stacklayout.addWidget(overview_page)

        # Add entry
        button2 = QAction("add entry", self)
        button2.triggered.connect(self.activate_tab_2)

        add_entry_page = AddEntryReportWindow()
        self.stacklayout.addWidget(add_entry_page)

        # Budget
        button3 = QAction("budget", self)
        button3.triggered.connect(self.activate_tab_3)

        budget_page = BudgetWindow()
        self.stacklayout.addWidget(budget_page)

        #view entries
        button4 = QAction("View Entries", self)
        button4.triggered.connect(self.activate_tab_4)
        
        view_entry = ViewEntryWindow()
        self.stacklayout.addWidget(view_entry)

        #view statistics
        button5 = QAction("Statistics", self)
        button5.triggered.connect(self.activate_tab_5)

        statistics_page = statisticsPage()
        self.stacklayout.addWidget(statistics_page)

        add_entry_page.data_saved.connect(overview_page.get_data)
        add_entry_page.data_saved.connect(view_entry.get_data)
        add_entry_page.data_saved.connect(statistics_page.get_data)

        #add actions to tool bar
        toolbar.addAction(button1)
        toolbar.addAction(button2)
        toolbar.addAction(button3)
        toolbar.addAction(button4)
        toolbar.addAction(button5)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # Start on the first page
        self.stacklayout.setCurrentIndex(1)

        #layers
    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(2)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(3)

    def activate_tab_4(self):
        self.stacklayout.setCurrentIndex(4)

    def activate_tab_5(self):
        self.stacklayout.setCurrentIndex(5)
app = QApplication([])
window = MainWindow()
window.showMaximized()
app.exec()