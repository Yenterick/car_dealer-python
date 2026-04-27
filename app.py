
import sys
from PyQt6.QtWidgets import QApplication

from db.Sqlite3Connection import Sqlite3Connection
from model.command.UndoRedoManager import UndoRedoManager

from service.BuyService import BuyService
from service.SaleService import SaleService
from service.CarService import CarService
from service.CustomerService import CustomerService
from service.SpareService import SpareService
from service.SupplierService import SupplierService
from service.EmployeeService import EmployeeService
from service.HistoryService import HistoryService

from controller.BuyController import BuyController
from controller.CarController import CarController
from controller.SaleController import SaleController
from controller.CustomerController import CustomerController
from controller.SpareControler import SpareController
from controller.SupplierController import SupplierController
from controller.EmployeeController import EmployeeController
from controller.HistoryController import HistoryController

from ui.mainWindow import MainWindow


def connection_factory() -> Sqlite3Connection:
    return Sqlite3Connection("db/car_dealer.db")


def build_controllers() -> dict:
    undo_manager: UndoRedoManager = UndoRedoManager()

    # Supplier
    supplier_service: SupplierService = SupplierService(connection_factory, undo_manager)
    supplier_controller: SupplierController = SupplierController(supplier_service)

    # Customer
    customer_service: CustomerService = CustomerService(connection_factory, undo_manager)
    customer_controller: CustomerController = CustomerController(customer_service)

    # Employee
    employee_service: EmployeeService = EmployeeService(connection_factory, undo_manager)
    employee_controller: EmployeeController = EmployeeController(employee_service)

    # Spare
    spare_service: SpareService = SpareService(connection_factory, undo_manager)
    spare_controller: SpareController = SpareController(spare_service)

    # Car
    car_service: CarService = CarService(connection_factory, undo_manager)
    car_controller: CarController = CarController(car_service)

    # Buy
    buy_service: BuyService = BuyService(connection_factory, undo_manager)
    buy_controller: BuyController = BuyController(buy_service)

    # Sale
    sale_service: SaleService = SaleService(connection_factory, undo_manager)
    sale_controller: SaleController = SaleController(sale_service)

    # History
    history_service: HistoryService = HistoryService(connection_factory, undo_manager)
    history_controller: HistoryController = HistoryController(history_service)

    return {
        'supplier': supplier_controller,
        'customer': customer_controller,
        'employee': employee_controller,
        'spare': spare_controller,
        'car': car_controller,
        'buy': buy_controller,
        'sale': sale_controller,
        'history': history_controller,
        'undo_manager': undo_manager
    }


def run():
    app = QApplication(sys.argv)
    controllers = build_controllers()
    window = MainWindow(controllers)
    window.show()
    sys.exit(app.exec())
