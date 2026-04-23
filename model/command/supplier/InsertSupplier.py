# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SupplierDAO import SupplierDAO
from model.vo.SupplierVO import SupplierVO

class InsertSupplier(Command):

    def __init__(self,
                 supplier: SupplierVO):
        self.supplier = supplier
        self.supplier_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the supplier
        if self.supplier_id is None:
            self.supplier_id = SupplierDAO.insert_supplier(
                connection,
                self.supplier
            )
        else:
            # We're reinserting the supplier
            SupplierDAO.reinsert_supplier(
                connection,
                self.supplier
            )

    def undo(self, connection: Sqlite3Connection):
        SupplierDAO.delete_supplier(
            self.supplier_id
        )
    
