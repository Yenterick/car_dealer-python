from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.SaleDialog import SaleDialog


class SalesView(BaseView):
    """View for managing sales"""

    def __init__(self, sale_controller, customer_controller=None,
                 employee_controller=None, car_controller=None,
                 spare_controller=None):
        self.sale_controller = sale_controller
        self.customer_controller = customer_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.spare_controller = spare_controller
        super().__init__(sale_controller)

    def load_data(self):
        try:
            sales = self.sale_controller.get_all_sales()
            self.table.setRowCount(0)

            if sales:
                for row_idx, sale in enumerate(sales):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(sale.sale_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(f"$ {sale.value:,.2f}"))
                    cust = f"{sale.customer.name} {sale.customer.last_name}" if sale.customer else ""
                    self.table.setItem(row_idx, 2, QTableWidgetItem(cust))
                    emp = f"{sale.employee.name} {sale.employee.last_name}" if sale.employee else ""
                    self.table.setItem(row_idx, 3, QTableWidgetItem(emp))
                    car_info = f"{sale.car.model} ({sale.car.year})" if sale.car else "—"
                    self.table.setItem(row_idx, 4, QTableWidgetItem(car_info))
                    spare_info = sale.spare.name if sale.spare else "—"
                    self.table.setItem(row_idx, 5, QTableWidgetItem(spare_info))
        except Exception as e:
            self.show_error("Error", f"Failed to load sales: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "Value", "Customer", "Employee", "Car", "Spare"]

    def get_column_count(self):
        return 6

    def on_add(self):
        needed = [self.customer_controller, self.employee_controller,
                  self.car_controller, self.spare_controller]
        if not all(needed):
            self.show_error("Error", "Required controllers not available")
            return
        dialog = SaleDialog(
            self.sale_controller, self.customer_controller,
            self.employee_controller, self.car_controller,
            self.spare_controller, None, self
        )
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Sale added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a sale to edit")
            return

        row = self.get_selected_row()
        sale_id = int(self.table.item(row, 0).text())

        try:
            sale = self.sale_controller.get_sale(sale_id)
            dialog = SaleDialog(
                self.sale_controller, self.customer_controller,
                self.employee_controller, self.car_controller,
                self.spare_controller, sale, self
            )
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Sale updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit sale: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a sale to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this sale?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            sale_id = int(self.table.item(row, 0).text())

            try:
                sale = self.sale_controller.get_sale(sale_id)
                self.sale_controller.delete_sale(sale)
                self.load_data()
                self.show_info("Success", "Sale deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete sale: {str(e)}")
