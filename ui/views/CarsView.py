from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from ui.views.BaseView import BaseView
from ui.dialogs.CarDialog import CarDialog


class CarsView(BaseView):
    """View for managing cars"""
    
    def __init__(self, car_controller, supplier_controller=None):
        self.car_controller = car_controller
        self.supplier_controller = supplier_controller
        super().__init__(car_controller)
        
    def load_data(self):
        """Load cars from controller"""
        try:
            cars = self.car_controller.get_all_cars()
            self.table.setRowCount(0)
            
            if cars:
                for row_idx, car in enumerate(cars):
                    self.table.insertRow(row_idx)
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(car.car_id)))
                    self.table.setItem(row_idx, 1, QTableWidgetItem(car.model))
                    self.table.setItem(row_idx, 2, QTableWidgetItem(str(car.year)))
                    self.table.setItem(row_idx, 3, QTableWidgetItem(car.type))
                    
                    supplier_name = car.supplier.name if car.supplier else "N/A"
                    self.table.setItem(row_idx, 4, QTableWidgetItem(supplier_name))
        except Exception as e:
            self.show_error("Error", f"Failed to load cars: {str(e)}")
        finally:
            self.on_search()
            
    def get_column_headers(self):
        """Return car table columns"""
        return ["ID", "Model", "Year", "Type", "Supplier"]
    
    def get_column_count(self):
        """Return number of columns"""
        return 5
    
    def on_add(self):
        """Open dialog to add new car"""
        dialog = CarDialog(self.car_controller, self.supplier_controller, None, self)
        if dialog.exec():
            self.load_data()
            self.show_info("Success", "Car added successfully")
    
    def on_edit(self):
        """Open dialog to edit selected car"""
        if not self.is_row_selected():
            self.show_error("Error", "Please select a car to edit")
            return
        
        row = self.get_selected_row()
        car_id = int(self.table.item(row, 0).text())
        
        try:
            car = self.car_controller.get_car(car_id)
            dialog = CarDialog(self.car_controller, self.supplier_controller, car, self)
            if dialog.exec():
                self.load_data()
                self.show_info("Success", "Car updated successfully")
        except Exception as e:
            self.show_error("Error", f"Failed to edit car: {str(e)}")
    
    def on_delete(self):
        """Delete selected car"""
        if not self.is_row_selected():
            self.show_error("Error", "Please select a car to delete")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this car?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = self.get_selected_row()
            car_id = int(self.table.item(row, 0).text())
            
            try:
                car = self.car_controller.get_car(car_id)
                self.car_controller.delete_car(car)
                self.load_data()
                self.show_info("Success", "Car deleted successfully")
            except Exception as e:
                self.show_error("Error", f"Failed to delete car: {str(e)}")
