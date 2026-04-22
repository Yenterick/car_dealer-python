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
