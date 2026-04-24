from typing import List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SupplierVO import SupplierVO

# Peewee VOs
from model.peewee.Supplier import Supplier

# DAOs for lazy loading
from model.dao.BuyDAO import BuyDAO
from model.dao.CarDAO import CarDAO
from model.dao.SpareDAO import SpareDAO

class SupplierDAO:

    @staticmethod
    def get_all_suppliers(connection: Sqlite3Connection) -> List[SupplierVO]:
        peewee_suppliers = Supplier.select()
        suppliers = []

        for peewee_supplier in peewee_suppliers:
            supplier = SupplierVO(
                supplier_id=peewee_supplier.supplier_id,
                name=peewee_supplier.name,
                email=peewee_supplier.email,
                phone=peewee_supplier.phone
            )

            supplier._buys_loader = lambda f=connection, s_id=peewee_supplier.supplier_id: BuyDAO.select_all_supplier_buys(f, s_id)
            supplier._cars_loader = lambda f=connection, s_id=peewee_supplier.supplier_id: CarDAO.select_all_supplier_cars(f, s_id)
            supplier._spares_loader = lambda f=connection, s_id=peewee_supplier.supplier_id: SpareDAO.select_all_supplier_spares(f, s_id)

            suppliers.append(supplier)
        return suppliers
    
    @staticmethod
    def get_supplier(connection: Sqlite3Connection, id: int) -> SupplierVO | None:
        peewee_supplier = Supplier.get_or_none(id)
        
        if peewee_supplier is None:
            return None

        return SupplierVO(
            supplier_id=peewee_supplier.supplier_id,
            name=peewee_supplier.name,
            email=peewee_supplier.email,
            phone=peewee_supplier.phone,
            _buys_loader=lambda: BuyDAO.select_all_supplier_buys(connection, peewee_supplier.supplier_id),
            _cars_loader=lambda: CarDAO.select_all_supplier_cars(connection, peewee_supplier.supplier_id),
            _spares_loader=lambda: SpareDAO.select_all_supplier_spares(connection, peewee_supplier.supplier_id)
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
    
    



