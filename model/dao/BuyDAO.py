from typing import Optional, List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.BuyVO import BuyVO
from model.vo.SupplierVO import SupplierVO
from model.vo.CarVO import CarVO
from model.vo.SpareVO import SpareVO

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
    
    @staticmethod
    def select_all_supplier_buys(connection: Sqlite3Connection,
                                 supplier_id: int) -> List[BuyVO] | None:
        
        query_string: str = '''
            SELECT  b.buy_id,
                    b.cost,
                    s.supplier_id,
                    s.name as supplier_name,
                    s.email,
                    s.phone,
                    c.car_id,
                    c.model,
                    c.year,
                    c.type as car_type,
                    sp.spare_id,
                    sp.name as spare_name,
                    sp.type as spare_type
            FROM buy b
            JOIN supplier s ON b.supplier_id = s.supplier_id
            LEFT JOIN car c ON b.car_id = c.car_id
            LEFT JOIN spare sp ON b.spare_id = sp.spare_id
            WHERE s.supplier_id = ? 
            '''
        
        cursor: Cursor = connection.execute(query_string,
                                            (
                                                supplier_id
                                            ))
        
        supplier_buys: List[BuyVO] = []

        for registry in cursor:

            loaded_registry: dict = dict(registry)

            supplier: SupplierVO = SupplierVO(
                    supplier_id=loaded_registry['supplier_id'],
                    name=loaded_registry['supplier_name'],
                    email=loaded_registry['email'],
                    phone=loaded_registry['phone']
            )

            car: CarVO | None = None
            if loaded_registry['car_id'] is not None:
                car = CarVO(
                    car_id=loaded_registry['car_id'],
                    model=loaded_registry['model'],
                    year=loaded_registry['year'],
                    type=loaded_registry['car_type'],
                    supplier=supplier
                )
            
            spare: SpareVO | None = None
            if loaded_registry['spare_id'] is not None:
                spare = SpareVO(
                    spare_id=loaded_registry['spare_id'],
                    name=loaded_registry['spare_name'],
                    type=loaded_registry['spare_type'],
                    supplier=supplier
                )

            buy: BuyVO = BuyVO(
                buy_id=loaded_registry['buy_id'],
                supplier=supplier,
                car=car,
                spare=spare,
                cost=loaded_registry['cost']
            )

            supplier_buys.append(buy)

        return supplier_buys
