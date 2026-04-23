from typing import Optional, List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.CarVO import CarVO
from model.vo.SupplierVO import SupplierVO

# Peewee VOs
from model.peewee.Car import Car

class CarDAO:

    @staticmethod
    def get_all_cars() -> List[Car]:
        return Car.select()
    
    @staticmethod
    def get_car(id: int) -> Car:
        return Car.get_by_id(id)
    
    @staticmethod
    def delete_car(id: int) -> None:
        Car.delete_by_id(id)

    @staticmethod
    def insert_car(connection: Sqlite3Connection,
                   car: CarVO,
                   supplier_id: int) -> int | None:

        query_string: str = 'INSERT INTO car (model, year, type, supplier_id) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                car.model,
                                                car.year,
                                                car.type,
                                                supplier_id 
                                           ))
        
        car_id = cursor.lastrowid
        return car_id
    
    @staticmethod
    def reinsert_car(connection: Sqlite3Connection,
                     car: CarVO,
                     supplier_id: int) -> int | None:
 
        query_string: str = 'INSERT INTO car (car_id, model, year, type, supplier_id) VALUES (?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                car.car_id,
                                                car.model,
                                                car.year,
                                                car.type,
                                                supplier_id 
                                           ))
        
        car_id = cursor.lastrowid
        return car_id
    
    @staticmethod
    def select_all_supplier_cars(connection: Sqlite3Connection,
                                 supplier_id: int) -> List[CarVO] | None:
        
        query_string: str = '''
            SELECT  c.car_id,
                    c.model,
                    c.year,
                    c.type,
                    s.supplier_id,
                    s.name,
                    s.email,
                    s.phone
            FROM car c 
            JOIN supplier s ON c.supplier_id = s.supplier_id
            WHERE s.supplier_id = ? 
            '''
        
        cursor: Cursor = connection.execute(query_string,
                                            (
                                                supplier_id
                                            ))
        
        supplier_cars: List[CarVO] = []

        for registry in cursor:

            loaded_registry: dict = dict(registry)

            supplier: SupplierVO = SupplierVO(
                    supplier_id=loaded_registry['supplier_id'],
                    name=loaded_registry['name'],
                    email=loaded_registry['email'],
                    phone=loaded_registry['phone']
            )

            car: CarVO = CarVO(
                car_id=loaded_registry['car_id'],
                model=loaded_registry['model'],
                year=loaded_registry['year'],
                type=loaded_registry['type'],
                supplier=supplier
            )

            supplier_cars.append(car)

        return supplier_cars