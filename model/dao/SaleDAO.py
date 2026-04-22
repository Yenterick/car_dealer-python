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
