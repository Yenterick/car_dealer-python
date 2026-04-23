from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.CarVO import CarVO

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
