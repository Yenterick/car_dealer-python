import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QPushButton, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from ui.views.CarsView import CarsView
from ui.views.CustomersView import CustomersView
from ui.views.EmployeesView import EmployeesView
from ui.views.SuppliersView import SuppliersView
from ui.views.SparesView import SparesView
from ui.views.BuysView import BuysView
from ui.views.SalesView import SalesView
from ui.views.HistoryView import HistoryView
from ui.stylesheet import MAIN_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.setWindowTitle("Car Dealer System")
        self.setGeometry(100, 100, 1400, 800)
        
        # Apply styles
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        toolbar_layout = QHBoxLayout()
        
        undo_btn = QPushButton("↶ Undo")
        redo_btn = QPushButton("↷ Redo")
        exit_btn = QPushButton("Exit")
        
        undo_btn.clicked.connect(self.undo_action)
        redo_btn.clicked.connect(self.redo_action)
        exit_btn.clicked.connect(self.close_application)
        
        toolbar_layout.addWidget(undo_btn)
        toolbar_layout.addWidget(redo_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(exit_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        
        self.cars_view = CarsView(self.controllers['car'], self.controllers['supplier'])
        self.customers_view = CustomersView(self.controllers['customer'])
        self.employees_view = EmployeesView(self.controllers['employee'])
        self.suppliers_view = SuppliersView(self.controllers['supplier'])
        self.spares_view = SparesView(
            self.controllers['spare'],
            self.controllers['supplier']
        )
        self.buys_view = BuysView(
            self.controllers['buy'],
            self.controllers['supplier'],
            self.controllers['car'],
            self.controllers['spare']
        )
        self.sales_view = SalesView(
            self.controllers['sale'],
            self.controllers['customer'],
            self.controllers['employee'],
            self.controllers['car'],
            self.controllers['spare']
        )
        self.history_view = HistoryView(self.controllers['history'])
        
        self.tabs.addTab(self.cars_view, "Cars")
        self.tabs.addTab(self.customers_view, "Customers")
        self.tabs.addTab(self.employees_view, "Employees")
        self.tabs.addTab(self.suppliers_view, "Suppliers")
        self.tabs.addTab(self.spares_view, "Spare Parts")
        self.tabs.addTab(self.buys_view, "Purchases")
        self.tabs.addTab(self.sales_view, "Sales")
        self.tabs.addTab(self.history_view, "History")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def undo_action(self):
        try:
            self.controllers['history'].undo()
            self._refresh_active_tab()
            self.statusBar().showMessage("Undo executed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Undo failed: {str(e)}")

    def redo_action(self):
        try:
            self.controllers['history'].redo()
            self._refresh_active_tab()
            self.statusBar().showMessage("Redo executed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Redo failed: {str(e)}")

    def _refresh_active_tab(self):
        """Refresh the data in the currently active tab"""
        current_widget = self.tabs.currentWidget()
        if hasattr(current_widget, 'load_data'):
            current_widget.load_data()
        
    def close_application(self):
        reply = QMessageBox.question(
            self, 
            'Exit',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
