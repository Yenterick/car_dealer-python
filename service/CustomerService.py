from typing import List, Callable

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.CustomerVO import CustomerVO
from model.dao.CustomerDAO import CustomerDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.customer.InsertCustomer import InsertCustomer
from model.command.customer.DeleteCustomer import DeleteCustomer

from ui.consoleUtils import log

class CustomerService:

    def __init__(self, 
                 connection_factory: Callable[[], Sqlite3Connection],
                 undo_manager: UndoRedoManager):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_customers(self) -> List[CustomerVO]:
        return CustomerDAO.get_all_customers()
    
    def get_customer(self, customer_id: int) -> CustomerVO | None:
        return CustomerDAO.get_customer(customer_id)

    def insert_customer(self, 
                        customer: CustomerVO):
        command = InsertCustomer(customer)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.register(command)

    def delete_customer(self,
                        customer: CustomerVO) -> None:
        command = DeleteCustomer(customer)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.push_redo(command)


