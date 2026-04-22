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
