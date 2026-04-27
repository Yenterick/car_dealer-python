from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QSpinBox, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class CarDialog(QDialog):
    """Dialog for adding/editing cars"""
    
    def __init__(self, car_controller, supplier_controller, car=None, parent=None):
        super().__init__(parent)
        self.car_controller = car_controller
        self.supplier_controller = supplier_controller
        self.car = car
        self.suppliers = []
        self.setWindowTitle("Car Details")
        self.setGeometry(100, 100, 400, 350)
        self.init_ui()
        
    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout(self)
        
        # Model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_input = QLineEdit()
        model_layout.addWidget(self.model_input)
        layout.addLayout(model_layout)
        
        # Year
        year_layout = QHBoxLayout()
        year_layout.addWidget(QLabel("Year:"))
        self.year_input = QSpinBox()
        self.year_input.setMinimum(1900)
        self.year_input.setMaximum(2100)
        self.year_input.setValue(2024)
        year_layout.addWidget(self.year_input)
        layout.addLayout(year_layout)
        
        # Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_input = QComboBox()
        self.type_input.addItems(["Sedan", "SUV", "Truck", "Coupe", "Van"])
        type_layout.addWidget(self.type_input)
        layout.addLayout(type_layout)
        
        # Supplier
        supplier_layout = QHBoxLayout()
        supplier_layout.addWidget(QLabel("Supplier:"))
        self.supplier_input = QComboBox()
        self._load_suppliers()
        supplier_layout.addWidget(self.supplier_input)
        layout.addLayout(supplier_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_car)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Load data if editing
        if self.car:
            self.model_input.setText(self.car.model)
            self.year_input.setValue(self.car.year)
            self.type_input.setCurrentText(self.car.type)
            if self.car.supplier:
                for i, s in enumerate(self.suppliers):
                    if s.supplier_id == self.car.supplier.supplier_id:
                        self.supplier_input.setCurrentIndex(i)
                        break

    def _load_suppliers(self):
        try:
            self.suppliers = self.supplier_controller.get_all_suppliers() or []
            for s in self.suppliers:
                self.supplier_input.addItem(f"{s.supplier_id} - {s.name}")
        except Exception:
            pass
    
    def save_car(self):
        """Save car"""
        try:
            model = self.model_input.text().strip()
            year = self.year_input.value()
            car_type = self.type_input.currentText()
            s_idx = self.supplier_input.currentIndex()
            
            if not model:
                QMessageBox.warning(self, "Validation", "Model is required")
                return
            if s_idx < 0 or not self.suppliers:
                QMessageBox.warning(self, "Validation", "Please select a supplier")
                return

            supplier = self.suppliers[s_idx]
            
            if self.car:
                # Update existing car (delete + insert pattern used in this project's commands)
                self.car_controller.delete_car(self.car)
                self.car_controller.insert_car(model, year, car_type, supplier)
            else:
                # Insert new car
                self.car_controller.insert_car(model, year, car_type, supplier)
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save car: {str(e)}")
