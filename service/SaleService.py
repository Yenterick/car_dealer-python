from typing import List

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.SaleVO import SaleVO
from model.dao.SaleDAO import SaleDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.sale.InsertSale import InsertSale
from model.command.sale.DeleteSale import DeleteSale

from ui.consoleUtils import log

class SaleService:

    def __init__(self, 
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_sales(self) -> List[SaleVO]:
        return SaleDAO.get_all_sales()
    
    def get_sale(self, sale_id: int) -> SaleVO | None:
        return SaleDAO.get_sale(sale_id)

    def select_all_employee_sales(self, employee_id: int) -> List[SaleVO] | None:
        return SaleDAO.select_all_employee_sales(self.connection, employee_id)

    def insert_sale(self, 
                    sale: SaleVO):
        command = InsertSale(sale)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_sale(self,
                    sale: SaleVO) -> None:
        command = DeleteSale(sale)

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
