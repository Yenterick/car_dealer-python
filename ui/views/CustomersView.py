from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.CustomerDialog import CustomerDialog


class CustomersView(BaseView):
    """View for managing customers"""

    def __init__(self, customer_controller):
        self.customer_controller = customer_controller
        super().__init__(customer_controller)

    def load_data(self):
        """Load customers from controller"""
        try:
            customers = self.customer_controller.get_all_customers()
            self.table.setRowCount(0)

            if customers:
                for row_idx, customer in enumerate(customers):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(customer.customer_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(customer.dni))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(customer.name))
                    self.table.setItem(row_idx, 3, QTableWidgetItem(customer.last_name))
        except Exception as e:
            self.show_error("Error", f"Failed to load customers: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "DNI", "Name", "Last Name"]

    def get_column_count(self):
        return 4

    def on_add(self):
        dialog = CustomerDialog(self.customer_controller, None, self)
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Customer added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a customer to edit")
            return

        row = self.get_selected_row()
        customer_id = int(self.table.item(row, 0).text())

        try:
            customer = self.customer_controller.get_customer(customer_id)
            dialog = CustomerDialog(self.customer_controller, customer, self)
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Customer updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit customer: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select a customer to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this customer?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            customer_id = int(self.table.item(row, 0).text())

            try:
                customer = self.customer_controller.get_customer(customer_id)
                self.customer_controller.delete_customer(customer)
                self.load_data()
                self.show_info("Success", "Customer deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete customer: {str(e)}")
