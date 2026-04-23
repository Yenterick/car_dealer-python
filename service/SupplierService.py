from typing import List

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.SupplierVO import SupplierVO
from model.dao.SupplierDAO import SupplierDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.supplier import InsertSupplier, DeleteSupplier

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
    
    
