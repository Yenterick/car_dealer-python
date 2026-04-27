from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QDoubleSpinBox, QComboBox, QPushButton, QMessageBox
)


class SaleDialog(QDialog):
    """Dialog for adding/editing sales"""

    def __init__(self, sale_controller, customer_controller, employee_controller,
                 car_controller, spare_controller, sale=None, parent=None):
        super().__init__(parent)
        self.sale_controller = sale_controller
        self.customer_controller = customer_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.spare_controller = spare_controller
        self.sale = sale
        self.customers = []
        self.employees = []
        self.cars = []
        self.spares = []
        self.setWindowTitle("Sale Details")
        self.setGeometry(100, 100, 450, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Value
        val_layout = QHBoxLayout()
        val_layout.addWidget(QLabel("Value:"))
        self.value_input = QDoubleSpinBox()
        self.value_input.setMinimum(0)
        self.value_input.setMaximum(999999999)
        self.value_input.setDecimals(2)
        self.value_input.setPrefix("$ ")
        val_layout.addWidget(self.value_input)
        layout.addLayout(val_layout)

        # Customer
        cust_layout = QHBoxLayout()
        cust_layout.addWidget(QLabel("Customer:"))
        self.customer_input = QComboBox()
        self._load_customers()
        cust_layout.addWidget(self.customer_input)
        layout.addLayout(cust_layout)

        # Employee
        emp_layout = QHBoxLayout()
        emp_layout.addWidget(QLabel("Employee:"))
        self.employee_input = QComboBox()
        self._load_employees()
        emp_layout.addWidget(self.employee_input)
        layout.addLayout(emp_layout)

        # Car (optional)
        car_layout = QHBoxLayout()
        car_layout.addWidget(QLabel("Car (optional):"))
        self.car_input = QComboBox()
        self.car_input.addItem("-- None --", None)
        self._load_cars()
        car_layout.addWidget(self.car_input)
        layout.addLayout(car_layout)

        # Spare (optional)
        spare_layout = QHBoxLayout()
        spare_layout.addWidget(QLabel("Spare (optional):"))
        self.spare_input = QComboBox()
        self.spare_input.addItem("-- None --", None)
        self._load_spares()
        spare_layout.addWidget(self.spare_input)
        layout.addLayout(spare_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_sale)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        if self.sale:
            self.value_input.setValue(self.sale.value)

    def _load_customers(self):
        try:
            self.customers = self.customer_controller.get_all_customers() or []
            for c in self.customers:
                self.customer_input.addItem(f"{c.customer_id} - {c.name} {c.last_name}")
        except Exception:
            pass

    def _load_employees(self):
        try:
            self.employees = self.employee_controller.get_all_employees() or []
            for e in self.employees:
                self.employee_input.addItem(f"{e.employee_id} - {e.name} {e.last_name}")
        except Exception:
            pass

    def _load_cars(self):
        try:
            self.cars = self.car_controller.get_all_cars() or []
            for c in self.cars:
                self.car_input.addItem(f"{c.car_id} - {c.model} ({c.year})")
        except Exception:
            pass

    def _load_spares(self):
        try:
            self.spares = self.spare_controller.get_all_spares() or []
            for sp in self.spares:
                self.spare_input.addItem(f"{sp.spare_id} - {sp.name}")
        except Exception:
            pass

    def save_sale(self):
        try:
            value = self.value_input.value()
            cu_idx = self.customer_input.currentIndex()
            em_idx = self.employee_input.currentIndex()
            ca_idx = self.car_input.currentIndex()
            sp_idx = self.spare_input.currentIndex()

            if value <= 0:
                QMessageBox.warning(self, "Validation", "Value must be > 0")
                return
            if cu_idx < 0 or not self.customers:
                QMessageBox.warning(self, "Validation", "Select a customer")
                return
            if em_idx < 0 or not self.employees:
                QMessageBox.warning(self, "Validation", "Select an employee")
                return

            customer = self.customers[cu_idx]
            employee = self.employees[em_idx]
            car = self.cars[ca_idx - 1] if ca_idx > 0 else None
            spare = self.spares[sp_idx - 1] if sp_idx > 0 else None

            if car is None and spare is None:
                QMessageBox.warning(self, "Validation", "Select at least a car or spare")
                return

            if self.sale:
                self.sale_controller.delete_sale(self.sale)
            self.sale_controller.insert_sale(value, customer, employee, car, spare)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
