from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.SupplierDialog import SupplierDialog


class SuppliersView(BaseView):
    """View for managing suppliers"""

    def __init__(self, supplier_controller):
        self.supplier_controller = supplier_controller
        super().__init__(supplier_controller)

    def load_data(self):
        try:
            suppliers = self.supplier_controller.get_all_suppliers()
            self.table.setRowCount(0)

            if suppliers:
                for row_idx, supplier in enumerate(suppliers):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(supplier.supplier_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(supplier.name))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(supplier.email))
                    self.table.setItem(row_idx, 3, QTableWidgetItem(supplier.phone))
        except Exception as e:
            self.show_error("Error", f"Failed to load suppliers: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "Name", "Email", "Phone"]

    def get_column_count(self):
        return 4

    def on_add(self):
        dialog = SupplierDialog(self.supplier_controller, None, self)
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Supplier added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a supplier to edit")
            return

        row = self.get_selected_row()
        supplier_id = int(self.table.item(row, 0).text())

        try:
            supplier = self.supplier_controller.get_supplier(supplier_id)
            dialog = SupplierDialog(self.supplier_controller, supplier, self)
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Supplier updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit supplier: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a supplier to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this supplier?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            supplier_id = int(self.table.item(row, 0).text())

            try:
                supplier = self.supplier_controller.get_supplier(supplier_id)
                self.supplier_controller.delete_supplier(supplier)
                self.load_data()
                self.show_info("Success", "Supplier deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete supplier: {str(e)}")
