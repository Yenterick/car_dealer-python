from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class CustomerDialog(QDialog):
    """Dialog for adding/editing customers"""

    def __init__(self, customer_controller, customer=None, parent=None):
        super().__init__(parent)
        self.customer_controller = customer_controller
        self.customer = customer
        self.setWindowTitle("Customer Details")
        self.setGeometry(100, 100, 400, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # DNI
        dni_layout = QHBoxLayout()
        dni_layout.addWidget(QLabel("DNI:"))
        self.dni_input = QLineEdit()
        dni_layout.addWidget(self.dni_input)
        layout.addLayout(dni_layout)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Last Name
        last_name_layout = QHBoxLayout()
        last_name_layout.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        last_name_layout.addWidget(self.last_name_input)
        layout.addLayout(last_name_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_customer)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        # Load data if editing
        if self.customer:
            self.dni_input.setText(self.customer.dni)
            self.name_input.setText(self.customer.name)
            self.last_name_input.setText(self.customer.last_name)

    def save_customer(self):
        try:
            dni = self.dni_input.text().strip()
            name = self.name_input.text().strip()
            last_name = self.last_name_input.text().strip()

            if not dni:
                QMessageBox.warning(self, "Validation", "DNI is required")
                return
            if not name:
                QMessageBox.warning(self, "Validation", "Name is required")
                return
            if not last_name:
                QMessageBox.warning(self, "Validation", "Last Name is required")
                return

            if self.customer:
                self.customer_controller.delete_customer(self.customer)
                self.customer_controller.insert_customer(dni, name, last_name)
            else:
                self.customer_controller.insert_customer(dni, name, last_name)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save customer: {str(e)}")
