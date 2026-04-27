from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QMessageBox, QHeaderView,
    QLineEdit, QLabel
)
from PyQt6.QtCore import Qt
from abc import ABCMeta, abstractmethod


class ABCQWidgetMeta(type(QWidget), ABCMeta):
    """Metaclass that combines PyQt6's QWidget metaclass with ABCMeta"""
    pass


class BaseView(QWidget, metaclass=ABCQWidgetMeta):
    """Base class for all views"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """Initialize the UI components"""
        self.main_layout = QVBoxLayout(self)
        
        # Search layout
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("🔍 Search by ID:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter ID to filter...")
        self.search_input.textChanged.connect(self.on_search)
        
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addStretch()

        # Button layout
        self.button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("➕ Add")
        self.edit_button = QPushButton("✏️ Edit")
        self.delete_button = QPushButton("🗑️ Delete")
        self.refresh_button = QPushButton("🔄 Refresh")
        
        self.add_button.clicked.connect(self.on_add)
        self.edit_button.clicked.connect(self.on_edit)
        self.delete_button.clicked.connect(self.on_delete)
        self.refresh_button.clicked.connect(self.load_data)
        
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.refresh_button)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(self.get_column_count())
        self.table.setHorizontalHeaderLabels(self.get_column_headers())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.table)
        
    @abstractmethod
    def load_data(self):
        """Load data from controller"""
        pass
    
    @abstractmethod
    def get_column_headers(self):
        """Return list of column headers"""
        pass
    
    @abstractmethod
    def get_column_count(self):
        """Return number of columns"""
        pass
    
    @abstractmethod
    def on_add(self):
        """Handle add button click"""
        pass
    
    @abstractmethod
    def on_edit(self):
        """Handle edit button click"""
        pass
    
    @abstractmethod
    def on_delete(self):
        """Handle delete button click"""
        pass
    
    def show_error(self, title, message):
        """Show error message dialog"""
        QMessageBox.critical(self, title, message)
        
    def show_info(self, title, message):
        """Show info message dialog"""
        QMessageBox.information(self, title, message)
        
    def get_selected_row(self):
        """Get selected row index"""
        return self.table.currentRow()
    
    def is_row_selected(self):
        """Check if a row is selected"""
        return self.table.currentRow() != -1

    def on_search(self):
        """Filter table rows by ID"""
        search_text = self.search_input.text().strip()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0) # ID is always at column 0
            if item:
                id_text = item.text()
                # Case-insensitive partial match
                if not search_text or search_text.lower() in id_text.lower():
                    self.table.setRowHidden(row, False)
                else:
                    self.table.setRowHidden(row, True)
