from typing import Optional, List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SpareVO import SpareVO
from model.vo.SupplierVO import SupplierVO

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

        query_string: str = 'INSERT INTO spare (name, type, supplier_id) VALUES (?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                spare.name,
                                                spare.type,
                                                supplier_id
                                           ))
        
        spare_id = cursor.lastrowid
        return spare_id
    
    @staticmethod
    def reinsert_spare(connection: Sqlite3Connection,
                       spare: SpareVO,
                       supplier_id: int) -> int | None:

        query_string: str = 'INSERT INTO spare (spare_id, name, type, supplier_id) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                spare.spare_id,
                                                spare.name,
                                                spare.type,
                                                supplier_id
                                           ))
        
        spare_id = cursor.lastrowid
        return spare_id
    
    @staticmethod
    def select_all_supplier_spares(connection: Sqlite3Connection,
                                   supplier_id: int) -> List[SpareVO] | None:
        
        query_string: str = '''
            SELECT  sp.spare_id,
                    sp.name,
                    sp.type,
                    s.supplier_id,
                    s.name as supplier_name,
                    s.email,
                    s.phone
            FROM spare sp 
            JOIN supplier s ON sp.supplier_id = s.supplier_id
            WHERE s.supplier_id = ? 
            '''
        
        cursor: Cursor = connection.execute(query_string,
                                            (
                                                supplier_id
                                            ))
        
        supplier_spares: List[SpareVO] = []

        for registry in cursor:

            loaded_registry: dict = dict(registry)

            supplier: SupplierVO = SupplierVO(
                    supplier_id=loaded_registry['supplier_id'],
                    name=loaded_registry['supplier_name'],
                    email=loaded_registry['email'],
                    phone=loaded_registry['phone']
            )

            spare: SpareVO = SpareVO(
                spare_id=loaded_registry['spare_id'],
                name=loaded_registry['name'],
                type=loaded_registry['type'],
                supplier=supplier
            )

            supplier_spares.append(spare)

        return supplier_spares