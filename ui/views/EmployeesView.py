from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ui.views.BaseView import BaseView
from ui.dialogs.EmployeeDialog import EmployeeDialog


class EmployeesView(BaseView):
    """View for managing employees"""

    def __init__(self, employee_controller):
        self.employee_controller = employee_controller
        super().__init__(employee_controller)

    def load_data(self):
        try:
            employees = self.employee_controller.get_all_employees()
            self.table.setRowCount(0)

            if employees:
                for row_idx, emp in enumerate(employees):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(emp.employee_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(emp.dni))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(emp.name))
                    self.table.setItem(row_idx, 3, QTableWidgetItem(emp.last_name))
        except Exception as e:
            self.show_error("Error", f"Failed to load employees: {str(e)}")
        finally:
            self.on_search()

    def get_column_headers(self):
        return ["ID", "DNI", "Name", "Last Name"]

    def get_column_count(self):
        return 4

    def on_add(self):
        dialog = EmployeeDialog(self.employee_controller, None, self)
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Employee added successfully")

    def on_edit(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select an employee to edit")
            return

        row = self.get_selected_row()
        employee_id = int(self.table.item(row, 0).text())

        try:
            employee = self.employee_controller.get_employee(employee_id)
            dialog = EmployeeDialog(self.employee_controller, employee, self)
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Employee updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit employee: {str(e)}")

    def on_delete(self):
        if not self.is_row_selected():
            self.show_error("Error", "Please select an employee to delete")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this employee?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            employee_id = int(self.table.item(row, 0).text())

            try:
                employee = self.employee_controller.get_employee(employee_id)
                self.employee_controller.delete_employee(employee)
                self.load_data()
                self.show_info("Success", "Employee deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete employee: {str(e)}")
