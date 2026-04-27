from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.SpareDialog import SpareDialog


class SparesView(BaseView):
    """View for managing spare parts"""

    def __init__(self, spare_controller, supplier_controller=None):
        self.spare_controller = spare_controller
        self.supplier_controller = supplier_controller
        super().__init__(spare_controller)

    def load_data(self):
        try:
            spares = self.spare_controller.get_all_spares()
            self.table.setRowCount(0)

            if spares:
                for row_idx, spare in enumerate(spares):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(spare.spare_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(spare.name))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(spare.type))
                    supplier_name = spare.supplier.name if spare.supplier else ""
                    self.table.setItem(row_idx, 3, QTableWidgetItem(supplier_name))
        except Exception as e:
            self.show_error("Error", f"Failed to load spares: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "Name", "Type", "Supplier"]

    def get_column_count(self):
        return 4

    def on_add(self):
        if not self.supplier_controller:
            self.show_error("Error", "Supplier controller not available")
            return
        dialog = SpareDialog(self.spare_controller, self.supplier_controller, None, self)
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Spare part added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a spare part to edit")
            return
        if not self.supplier_controller:
            self.show_error("Error", "Supplier controller not available")
            return

        row = self.get_selected_row()
        spare_id = int(self.table.item(row, 0).text())

        try:
            spare = self.spare_controller.get_spare(spare_id)
            dialog = SpareDialog(self.spare_controller, self.supplier_controller, spare, self)
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Spare part updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit spare: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a spare part to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this spare part?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            spare_id = int(self.table.item(row, 0).text())

            try:
                spare = self.spare_controller.get_spare(spare_id)
                self.spare_controller.delete_spare(spare)
                self.load_data()
                self.show_info("Success", "Spare part deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete spare: {str(e)}")
