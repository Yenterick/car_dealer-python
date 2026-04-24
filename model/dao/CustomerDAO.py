from typing import List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.CustomerVO import CustomerVO

# Peewee VOs
from model.peewee.Customer import Customer

# DAOs for lazy loading
from model.dao.SaleDAO import SaleDAO

class CustomerDAO:

    @staticmethod
    def get_all_customers(connection: Sqlite3Connection) -> List[CustomerVO]:
        peewee_customers = Customer.select()
        customers = []

        for peewee_customer in peewee_customers:
            customer = CustomerVO(
                customer_id=peewee_customer.customer_id,
                dni=peewee_customer.dni,
                name=peewee_customer.name,
                last_name=peewee_customer.last_name
            )

            customer._sales_loader = lambda f=connection, c_id=peewee_customer.customer_id: SaleDAO.select_all_customer_sales(f, c_id)
            customers.append(customer)
        return customers
    
    @staticmethod
    def get_customer(connection: Sqlite3Connection, id: int) -> CustomerVO | None:
        peewee_customer = Customer.get_or_none(id)
        
        if peewee_customer is None:
            return None

        return CustomerVO(
            customer_id=peewee_customer.customer_id,
            dni=peewee_customer.dni,
            name=peewee_customer.name,
            last_name=peewee_customer.last_name,
            _sales_loader=lambda: SaleDAO.select_all_customer_sales(connection, peewee_customer.customer_id)
        )
    
    @staticmethod
    def delete_customer(id: int | None) -> None:
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
