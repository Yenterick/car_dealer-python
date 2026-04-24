# Project imports
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

def connection_factory() -> Sqlite3Connection:
    return Sqlite3Connection("db/car_dealer.db")

def build_controllers() -> dict:
    undo_manager: UndoRedoManager = UndoRedoManager()

    supplier_service: SupplierService = SupplierService(connection_factory, undo_manager)
    supplier_controller: SupplierController = SupplierController(supplier_service)

    customer_service: CustomerService = CustomerService(connection_factory, undo_manager)
    customer_controller: CustomerController = CustomerController(customer_service)

    employee_service: EmployeeService = EmployeeService(connection_factory, undo_manager)
    employee_controller: EmployeeController = EmployeeController(employee_service)

    spare_service: SpareService = SpareService(connection_factory, undo_manager)
    spare_controller: SpareController = SpareController(spare_service)

    car_service: CarService = CarService(connection_factory, undo_manager)
    car_controller: CarController = CarController(car_service)

    buy_service: BuyService = BuyService(connection_factory, undo_manager)
    buy_controller: BuyController = BuyController(buy_service)

    sale_service: SaleService = SaleService(connection_factory, undo_manager)
    sale_controller: SaleController = SaleController(sale_service)

    history_service: HistoryService = HistoryService(connection_factory, undo_manager)
    history_controller: HistoryController = HistoryController(history_service)

    return {
        "buy_controller": buy_controller,
        "car_controller": car_controller,
        "spare_controller": spare_controller,
        "supplier_controller": supplier_controller,
        "employee_controller": employee_controller,
        "sale_controller": sale_controller,
        "customer_controller": customer_controller,
        "history_controller": history_controller
    }

def main():
    controllers: dict = build_controllers()

if __name__ == "__main__":
    main()