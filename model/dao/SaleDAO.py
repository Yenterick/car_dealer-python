from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SaleVO import SaleVO

# Peewee VOs
from model.peewee.Sale import Sale

class SaleDAO:

    @staticmethod
    def get_all_sales() -> List[Sale]:
        return Sale.select()
    
    @staticmethod
    def get_sale(id: int) -> Sale:
        return Sale.get_by_id(id)
    
    @staticmethod
    def delete_sale(id: int) -> None:
        Sale.delete_by_id(id)

    @staticmethod
    def insert_sale(connection: Sqlite3Connection,
                    sale: SaleVO,
                    customer_id: int,
                    car_id: Optional[int],
                    spare_id: Optional[int],
                    employee_id: int) -> int | None:
  
        query_string: str = 'INSERT INTO sale (value, customer_id, car_id, spare_id, employee_id) VALUES (?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                sale.value,
                                                customer_id,
                                                car_id,
                                                spare_id,
                                                employee_id
                                           ))
        
        sale_id = cursor.lastrowid
        return sale_id
    
    @staticmethod
    def reinsert_sale(connection: Sqlite3Connection,
                      sale: SaleVO,
                      customer_id: int,
                      car_id: Optional[int],
                      spare_id: Optional[int],
                      employee_id: int) -> int | None:
  
        query_string: str = 'INSERT INTO sale (sale_id, value, customer_id, car_id, spare_id, employee_id) VALUES (?, ?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                sale.sale_id,
                                                sale.value,
                                                customer_id,
                                                car_id,
                                                spare_id,
                                                employee_id
                                           ))
        
        sale_id = cursor.lastrowid
        return sale_id
