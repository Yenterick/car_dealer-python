from typing import List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SupplierVO import SupplierVO

# Peewee VOs
from model.peewee.Supplier import Supplier

class SupplierDAO:

    @staticmethod
    def get_all_suppliers() -> List[SupplierVO]:
        peewee_suppliers = Supplier.select()
        suppliers = []
        for peewee_supplier in peewee_suppliers:
            suppliers.append(SupplierVO(
                supplier_id=peewee_supplier.supplier_id,
                name=peewee_supplier.name,
                email=peewee_supplier.email,
                phone=peewee_supplier.phone
            ))
        return suppliers
    
    @staticmethod
    def get_supplier(id: int) -> SupplierVO | None:
        peewee_supplier = Supplier.get_or_none(id)
        
        if peewee_supplier is None:
            return None

        return SupplierVO(
            supplier_id=peewee_supplier.supplier_id,
            name=peewee_supplier.name,
            email=peewee_supplier.email,
            phone=peewee_supplier.phone
        )
    
    @staticmethod
    def delete_supplier(id: int | None) -> None:
        Supplier.delete_by_id(id)

    @staticmethod
    def insert_supplier(connection: Sqlite3Connection,
                        supplier: SupplierVO) -> int | None:
   
        query_string: str = 'INSERT INTO supplier (name, email, phone) VALUES (?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                supplier.name,
                                                supplier.email,
                                                supplier.phone
                                           ))

        supplier_id = cursor.lastrowid
        return supplier_id
    
    @staticmethod
    def reinsert_supplier(connection: Sqlite3Connection, 
                          supplier: SupplierVO) -> int | None:
   
        query_string: str = 'INSERT INTO supplier (supplier_id, name, email, phone) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                supplier.supplier_id,
                                                supplier.name,
                                                supplier.email,
                                                supplier.phone
                                           ))

        supplier_id = cursor.lastrowid
        return supplier_id
    
    



