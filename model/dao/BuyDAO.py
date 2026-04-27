from typing import List
from sqlite3 import Cursor
from peewee import JOIN

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.BuyVO import BuyVO
from model.vo.SupplierVO import SupplierVO
from model.vo.CarVO import CarVO
from model.vo.SpareVO import SpareVO

# Peewee VOs
from model.peewee.Buy import Buy
from model.peewee.Car import Car
from model.peewee.Spare import Spare
from model.peewee.Supplier import Supplier

class BuyDAO:

    @staticmethod
    def get_all_buys() -> List[BuyVO]:
        peewee_buys = (Buy
                       .select(Buy, Supplier, Car, Spare)
                       .join(Supplier).switch(Buy)
                       .join(Car, JOIN.LEFT_OUTER).switch(Buy)
                       .join(Spare, JOIN.LEFT_OUTER))
        buys = []
        for peewee_buy in peewee_buys:
            supplier_vo = None
            
            # Needs to check inside of a try block bc if the data is missing it goes crazy
            try:
                supplier_vo = SupplierVO(
                    supplier_id=peewee_buy.supplier_id.supplier_id,
                    name=peewee_buy.supplier_id.name,
                    email=peewee_buy.supplier_id.email,
                    phone=peewee_buy.supplier_id.phone
                )
            except Exception:
                pass
            
            car_vo = None
            try:
                if peewee_buy.car_id is not None:
                    car_supplier = SupplierVO(
                        supplier_id=peewee_buy.car_id.supplier_id.supplier_id,
                        name=peewee_buy.car_id.supplier_id.name,
                        email=peewee_buy.car_id.supplier_id.email,
                        phone=peewee_buy.car_id.supplier_id.phone
                    )
                    car_vo = CarVO(
                        car_id=peewee_buy.car_id.car_id,
                        model=peewee_buy.car_id.model,
                        year=peewee_buy.car_id.year,
                        type=peewee_buy.car_id.type,
                        supplier=car_supplier
                    )
            except Exception:
                car_vo = None
            
            spare_vo = None
            try:
                if peewee_buy.spare_id is not None:
                    spare_supplier = SupplierVO(
                        supplier_id=peewee_buy.spare_id.supplier_id.supplier_id,
                        name=peewee_buy.spare_id.supplier_id.name,
                        email=peewee_buy.spare_id.supplier_id.email,
                        phone=peewee_buy.spare_id.supplier_id.phone
                    )
                    spare_vo = SpareVO(
                        spare_id=peewee_buy.spare_id.spare_id,
                        name=peewee_buy.spare_id.name,
                        type=peewee_buy.spare_id.type,
                        supplier=spare_supplier
                    )
            except Exception:
                spare_vo = None

            buys.append(BuyVO(
                buy_id=peewee_buy.buy_id,
                supplier=supplier_vo,
                car=car_vo,
                spare=spare_vo,
                cost=peewee_buy.cost
            ))
        return buys
    
    @staticmethod
    def get_buy(id: int) -> BuyVO | None:
        peewee_buy = (Buy
                      .select(Buy, Supplier, Car, Spare)
                      .join(Supplier).switch(Buy)
                      .join(Car, JOIN.LEFT_OUTER).switch(Buy)
                      .join(Spare, JOIN.LEFT_OUTER)
                      .where(Buy.buy_id == id)
                      .first())
        
        if peewee_buy is None:
            return None

        supplier_vo = SupplierVO(
            supplier_id=peewee_buy.supplier_id.supplier_id,
            name=peewee_buy.supplier_id.name,
            email=peewee_buy.supplier_id.email,
            phone=peewee_buy.supplier_id.phone
        )
        
        supplier_vo = None
        try:
            supplier_vo = SupplierVO(
                supplier_id=peewee_buy.supplier_id.supplier_id,
                name=peewee_buy.supplier_id.name,
                email=peewee_buy.supplier_id.email,
                phone=peewee_buy.supplier_id.phone
            )
        except Exception:
            pass
        
        car_vo = None
        try:
            if peewee_buy.car_id is not None:
                car_supplier = SupplierVO(
                    supplier_id=peewee_buy.car_id.supplier_id.supplier_id,
                    name=peewee_buy.car_id.supplier_id.name,
                    email=peewee_buy.car_id.supplier_id.email,
                    phone=peewee_buy.car_id.supplier_id.phone
                )
                car_vo = CarVO(
                    car_id=peewee_buy.car_id.car_id,
                    model=peewee_buy.car_id.model,
                    year=peewee_buy.car_id.year,
                    type=peewee_buy.car_id.type,
                    supplier=car_supplier
                )
        except Exception:
            car_vo = None
        
        spare_vo = None
        try:
            if peewee_buy.spare_id is not None:
                spare_supplier = SupplierVO(
                    supplier_id=peewee_buy.spare_id.supplier_id.supplier_id,
                    name=peewee_buy.spare_id.supplier_id.name,
                    email=peewee_buy.spare_id.supplier_id.email,
                    phone=peewee_buy.spare_id.supplier_id.phone
                )
                spare_vo = SpareVO(
                    spare_id=peewee_buy.spare_id.spare_id,
                    name=peewee_buy.spare_id.name,
                    type=peewee_buy.spare_id.type,
                    supplier=spare_supplier
                )
        except Exception:
            spare_vo = None

        return BuyVO(
            buy_id=peewee_buy.buy_id,
            supplier=supplier_vo,
            car=car_vo,
            spare=spare_vo,
            cost=peewee_buy.cost
        )
    
    @staticmethod
    def delete_buy(id: int | None) -> None:
        if id is not None:
            Buy.delete_by_id(id)

    @staticmethod
    def insert_buy(connection: Sqlite3Connection,
                   buy: BuyVO) -> int | None:
  
        query_string: str = 'INSERT INTO buy (cost, supplier_id, car_id, spare_id) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                buy.cost,
                                                buy.supplier.supplier_id if buy.supplier else None,
                                                buy.car.car_id if buy.car else None,
                                                buy.spare.spare_id if buy.spare else None
                                           ))
        
        buy_id = cursor.lastrowid
        return buy_id

    @staticmethod
    def reinsert_buy(connection: Sqlite3Connection,
                     buy: BuyVO) -> int | None:
  
        query_string: str = 'INSERT INTO buy (buy_id, cost, supplier_id, car_id, spare_id) VALUES (?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                buy.buy_id,
                                                buy.cost,
                                                buy.supplier.supplier_id if buy.supplier else None,
                                                buy.car.car_id if buy.car else None,
                                                buy.spare.spare_id if buy.spare else None
                                           ))
        
        buy_id = cursor.lastrowid
        return buy_id
    
    @staticmethod
    def select_all_supplier_buys(connection: Sqlite3Connection,
                                 supplier_id: int) -> List[BuyVO]:
        
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
                                                supplier_id,
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
