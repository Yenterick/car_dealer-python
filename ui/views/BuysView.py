from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.BuyDialog import BuyDialog


class BuysView(BaseView):
    """View for managing purchases"""

    def __init__(self, buy_controller, supplier_controller=None,
                 car_controller=None, spare_controller=None):
        self.buy_controller = buy_controller
        self.supplier_controller = supplier_controller
        self.car_controller = car_controller
        self.spare_controller = spare_controller
        super().__init__(buy_controller)

    def load_data(self):
        try:
            buys = self.buy_controller.get_all_buys()
            self.table.setRowCount(0)

            if buys:
                for row_idx, buy in enumerate(buys):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(buy.buy_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(f"$ {buy.cost:,.2f}"))
                    supplier_name = buy.supplier.name if buy.supplier else ""
                    self.table.setItem(row_idx, 2, QTableWidgetItem(supplier_name))
                    car_info = f"{buy.car.model} ({buy.car.year})" if buy.car else "—"
                    self.table.setItem(row_idx, 3, QTableWidgetItem(car_info))
                    spare_info = buy.spare.name if buy.spare else "—"
                    self.table.setItem(row_idx, 4, QTableWidgetItem(spare_info))
        except Exception as e:
            self.show_error("Error", f"Failed to load purchases: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "Cost", "Supplier", "Car", "Spare"]

    def get_column_count(self):
        return 5

    def on_add(self):
        if not all([self.supplier_controller, self.car_controller, self.spare_controller]):
            self.show_error("Error", "Required controllers not available")
            return
        dialog = BuyDialog(
            self.buy_controller, self.supplier_controller,
            self.car_controller, self.spare_controller, None, self
        )
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Purchase added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a purchase to edit")
            return
        if not all([self.supplier_controller, self.car_controller, self.spare_controller]):
            self.show_error("Error", "Required controllers not available")
            return

        row = self.get_selected_row()
        buy_id = int(self.table.item(row, 0).text())

        try:
            buy = self.buy_controller.get_buy(buy_id)
            dialog = BuyDialog(
                self.buy_controller, self.supplier_controller,
                self.car_controller, self.spare_controller, buy, self
            )
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Purchase updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit purchase: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a purchase to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this purchase?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            buy_id = int(self.table.item(row, 0).text())

            try:
                buy = self.buy_controller.get_buy(buy_id)
                self.buy_controller.delete_buy(buy)
                self.load_data()
                self.show_info("Success", "Purchase deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete purchase: {str(e)}")
