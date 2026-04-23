# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.SupplierDAO import SupplierDAO
from model.vo.SupplierVO import SupplierVO

class DeleteSupplier(Command):

    def __init__(self,
                 supplier: SupplierVO):
        self.supplier = supplier
        self.supplier_id = None

    def redo(self, connection: Sqlite3Connection):
        self.supplier_id = self.supplier.supplier_id
        SupplierDAO.delete_supplier(self.supplier_id)

    def undo(self, connection: Sqlite3Connection):
        SupplierDAO.reinsert_supplier(
            connection,
            self.supplier
        )

