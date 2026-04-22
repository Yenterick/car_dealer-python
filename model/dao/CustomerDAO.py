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
