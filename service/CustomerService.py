from typing import List

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
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_customers(self) -> List[CustomerVO]:
        return CustomerDAO.get_all_customers()
    
    def get_customer(self, customer_id: int) -> CustomerVO | None:
        return CustomerDAO.get_customer(customer_id)

    def insert_customer(self, 
                        customer: CustomerVO):
        command = InsertCustomer(customer)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_customer(self,
                        customer: CustomerVO) -> None:
        command = DeleteCustomer(customer)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_redo(command)

    def undo(self) -> None:
        command = self.undo_manager.get_undo()
        if command is None:
            log("There's nothing to undo.")
            return
        
        with self.connection:
            command.undo(self.connection)

        self.undo_manager.push_redo(command)
        
    def redo(self) -> None:
        command = self.undo_manager.get_redo()
        if command is None:
            log("There's nothing to redo.")
            return
        
        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_undo(command)
