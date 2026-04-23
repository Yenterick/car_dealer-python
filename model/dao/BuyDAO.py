from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.BuyVO import BuyVO

# Peewee VOs
from model.peewee.Buy import Buy

class BuyDAO:

    @staticmethod
    def get_all_buys() -> List[Buy]:
        return Buy.select()
    
    @staticmethod
    def get_buy(id: int) -> Buy:
        return Buy.get_by_id(id)
    
    @staticmethod
    def delete_buy(id: int) -> None:
        Buy.delete_by_id(id)

    @staticmethod
    def insert_buy(connection: Sqlite3Connection,
                   buy: BuyVO,
                   supplier_id: int,
                   car_id: Optional[int],
                   spare_id: Optional[int]) -> int | None:

        query_string: str = 'INSERT INTO buy (cost, supplier_id, car_id, spare_id) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                buy.cost,
                                                supplier_id,
                                                car_id,
                                                spare_id
                                           ))
        
        buy_id = cursor.lastrowid
        return buy_id
    
    @staticmethod
    def reinsert_buy(connection: Sqlite3Connection,
                     buy: BuyVO,
                     supplier_id: int,
                     car_id: Optional[int],
                     spare_id: Optional[int]) -> int | None:

        query_string: str = 'INSERT INTO buy (buy_id, cost, supplier_id, car_id, spare_id) VALUES (?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                buy.buy_id,
                                                buy.cost,
                                                supplier_id,
                                                car_id,
                                                spare_id
                                           ))
        
        buy_id = cursor.lastrowid
        return buy_id
