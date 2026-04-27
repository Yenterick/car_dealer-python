from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QDoubleSpinBox, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class BuyDialog(QDialog):
    """Dialog for adding/editing purchases"""

    def __init__(self, buy_controller, supplier_controller, car_controller,
                 spare_controller, buy=None, parent=None):
        super().__init__(parent)
        self.buy_controller = buy_controller
        self.supplier_controller = supplier_controller
        self.car_controller = car_controller
        self.spare_controller = spare_controller
        self.buy = buy
        self.suppliers = []
        self.cars = []
        self.spares = []
        self.setWindowTitle("Purchase Details")
        self.setGeometry(100, 100, 450, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Cost
        cost_layout = QHBoxLayout()
        cost_layout.addWidget(QLabel("Cost:"))
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMinimum(0)
        self.cost_input.setMaximum(999999999)
        self.cost_input.setDecimals(2)
        self.cost_input.setPrefix("$ ")
        cost_layout.addWidget(self.cost_input)
        layout.addLayout(cost_layout)

        # Supplier
        supplier_layout = QHBoxLayout()
        supplier_layout.addWidget(QLabel("Supplier:"))
        self.supplier_input = QComboBox()
        self._load_suppliers()
        supplier_layout.addWidget(self.supplier_input)
        layout.addLayout(supplier_layout)

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
        save_btn.clicked.connect(self.save_buy)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        # Pre-fill when editing
        if self.buy:
            self.cost_input.setValue(self.buy.cost)

    def _load_suppliers(self):
        try:
            self.suppliers = self.supplier_controller.get_all_suppliers() or []
            for s in self.suppliers:
                self.supplier_input.addItem(f"{s.supplier_id} - {s.name}")
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

    def save_buy(self):
        try:
            cost = self.cost_input.value()
            s_idx = self.supplier_input.currentIndex()
            c_idx = self.car_input.currentIndex()
            sp_idx = self.spare_input.currentIndex()

            if cost <= 0:
                QMessageBox.warning(self, "Validation", "Cost must be > 0")
                return
            if s_idx < 0 or not self.suppliers:
                QMessageBox.warning(self, "Validation", "Select a supplier")
                return

            supplier = self.suppliers[s_idx]
            car = self.cars[c_idx - 1] if c_idx > 0 else None
            spare = self.spares[sp_idx - 1] if sp_idx > 0 else None

            if car is None and spare is None:
                QMessageBox.warning(self, "Validation", "Select at least a car or spare")
                return

            if self.buy:
                self.buy_controller.delete_buy(self.buy)
            self.buy_controller.insert_buy(cost, supplier, car, spare)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
