from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SupplierVO import SupplierVO

# Peewee VOs
from model.peewee.Supplier import Supplier

class SupplierDAO:

    @staticmethod
    def get_all_suppliers() -> List[Supplier]:
        return Supplier.select()
    
    @staticmethod
    def get_supplier(id: int) -> Supplier:
        return Supplier.get_by_id(id)
    
    @staticmethod
    def delete_supplier(id: int) -> None:
        Supplier.delete_by_id(id)