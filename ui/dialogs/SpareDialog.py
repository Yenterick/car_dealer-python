from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class SpareDialog(QDialog):
    """Dialog for adding/editing spare parts"""

    def __init__(self, spare_controller, supplier_controller, spare=None, parent=None):
        super().__init__(parent)
        self.spare_controller = spare_controller
        self.supplier_controller = supplier_controller
        self.spare = spare
        self.suppliers = []
        self.setWindowTitle("Spare Part Details")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_input = QComboBox()
        self.type_input.addItems([
            "Motor", "Frenos", "Suspensión", "Eléctrico",
            "Refrigeración", "Transmisión", "Carrocería", "Otro"
        ])
        self.type_input.setEditable(True)
        type_layout.addWidget(self.type_input)
        layout.addLayout(type_layout)

        # Supplier
        supplier_layout = QHBoxLayout()
        supplier_layout.addWidget(QLabel("Supplier:"))
        self.supplier_input = QComboBox()
        self.load_suppliers()
        supplier_layout.addWidget(self.supplier_input)
        layout.addLayout(supplier_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_spare)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        # Load data if editing
        if self.spare:
            self.name_input.setText(self.spare.name)
            self.type_input.setCurrentText(self.spare.type)
            if self.spare.supplier:
                for i, s in enumerate(self.suppliers):
                    if s.supplier_id == self.spare.supplier.supplier_id:
                        self.supplier_input.setCurrentIndex(i)
                        break

    def load_suppliers(self):
        try:
            self.suppliers = self.supplier_controller.get_all_suppliers() or []
            for supplier in self.suppliers:
                self.supplier_input.addItem(
                    f"{supplier.supplier_id} - {supplier.name}",
                    supplier.supplier_id
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load suppliers: {str(e)}")

    def save_spare(self):
        try:
            name = self.name_input.text().strip()
            spare_type = self.type_input.currentText().strip()
            supplier_idx = self.supplier_input.currentIndex()

            if not name:
                QMessageBox.warning(self, "Validation", "Name is required")
                return
            if not spare_type:
                QMessageBox.warning(self, "Validation", "Type is required")
                return
            if supplier_idx < 0 or not self.suppliers:
                QMessageBox.warning(self, "Validation", "Please select a supplier")
                return

            supplier = self.suppliers[supplier_idx]

            if self.spare:
                self.spare_controller.delete_spare(self.spare)
                self.spare_controller.insert_spare(name, spare_type, supplier)
            else:
                self.spare_controller.insert_spare(name, spare_type, supplier)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save spare: {str(e)}")
