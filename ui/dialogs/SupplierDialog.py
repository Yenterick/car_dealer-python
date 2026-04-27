import re
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class SupplierDialog(QDialog):
    """Dialog for adding/editing suppliers"""

    def __init__(self, supplier_controller, supplier=None, parent=None):
        super().__init__(parent)
        self.supplier_controller = supplier_controller
        self.supplier = supplier
        self.setWindowTitle("Supplier Details")
        self.setGeometry(100, 100, 400, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Email
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # Phone
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_supplier)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        # Load data if editing
        if self.supplier:
            self.name_input.setText(self.supplier.name)
            self.email_input.setText(self.supplier.email)
            self.phone_input.setText(self.supplier.phone)

    def save_supplier(self):
        try:
            name = self.name_input.text().strip()
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()

            if not name:
                QMessageBox.warning(self, "Validation", "Name is required")
                return
            if not email:
                QMessageBox.warning(self, "Validation", "Email is required")
                return
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                QMessageBox.warning(self, "Validation", "Invalid email format")
                return
            if not phone:
                QMessageBox.warning(self, "Validation", "Phone is required")
                return

            if self.supplier:
                # Update existing
                self.supplier.name = name
                self.supplier.email = email
                self.supplier.phone = phone
                # Re-insert as update (delete + insert pattern)
                self.supplier_controller.delete_supplier(self.supplier)
                self.supplier_controller.insert_supplier(name, email, phone)
            else:
                self.supplier_controller.insert_supplier(name, email, phone)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save supplier: {str(e)}")
