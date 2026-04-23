from typing import List

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.SupplierVO import SupplierVO
from model.dao.SupplierDAO import SupplierDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.supplier.InsertSupplier import InsertSupplier
from model.command.supplier.DeleteSupplier import DeleteSupplier

from ui.consoleUtils import log

class SupplierService:

    def __init__(self, 
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_suppliers(self) -> List[SupplierVO]:
        return SupplierDAO.get_all_suppliers()
    
    def get_supplier(self, supplier_id: int) -> SupplierVO | None:
        return SupplierDAO.get_supplier(supplier_id)

    def insert_supplier(self, 
                        supplier: SupplierVO):
        command = InsertSupplier(supplier)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_supplier(self,
                        supplier: SupplierVO) -> None:
        command = DeleteSupplier(supplier)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_redo(command)



