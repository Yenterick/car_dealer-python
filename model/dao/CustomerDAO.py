from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.CustomerVO import CustomerVO

# Peewee VOs
from model.peewee.Customer import Customer

class CustomerDAO:

    @staticmethod
    def get_all_customers() -> List[Customer]:
        return Customer.select()
    
    @staticmethod
    def get_customer(id: int) -> Customer:
        return Customer.get_by_id(id)
    
    @staticmethod
    def delete_customer(id: int) -> None:
        Customer.delete_by_id(id)

    @staticmethod
    def insert_customer(connection: Sqlite3Connection,
                        customer: CustomerVO) -> int | None:
   
        query_string: str = 'INSERT INTO customer (dni, name, last_name) VALUES (?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                customer.dni,
                                                customer.name,
                                                customer.last_name
                                           ))
        
        customer_id = cursor.lastrowid
        return customer_id
    
    @staticmethod
    def reinsert_customer(connection: Sqlite3Connection,
                          customer: CustomerVO) -> int | None:

        query_string: str = 'INSERT INTO customer (customer_id, dni, name, last_name) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                customer.customer_id,
                                                customer.dni,
                                                customer.name,
                                                customer.last_name
                                           ))
        
        customer_id = cursor.lastrowid
        return customer_id
