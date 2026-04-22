from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SpareVO import SpareVO

# Peewee VOs
from model.peewee.Spare import Spare

class SpareDAO:

    @staticmethod
    def get_all_spares() -> List[Spare]:
        return Spare.select()
    
    @staticmethod
    def get_spare(id: int) -> Spare:
        return Spare.get_by_id(id)
    
    @staticmethod
    def delete_spare(id: int) -> None:
        Spare.delete_by_id(id)

    @staticmethod
    def insert_spare(connection: Sqlite3Connection,
                     spare: SpareVO,
                     supplier_id: int) -> int | None:
        # TODO: Implement query string
        query_string: str = ''

        cursor: Cursor = connection.cursor(query_string,
                                           (
                                                spare.name,
                                                spare.type,
                                                supplier_id
                                           ))
        