from typing import List

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.CarVO import CarVO
from model.dao.CarDAO import CarDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.car.InsertCar import InsertCar
from model.command.car.DeleteCar import DeleteCar

from ui.consoleUtils import log

class CarService:

    def __init__(self, 
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_cars(self) -> List[CarVO]:
        return CarDAO.get_all_cars()
    
    def get_car(self, car_id: int) -> CarVO | None:
        return CarDAO.get_car(car_id)

    def select_all_supplier_cars(self, supplier_id: int) -> List[CarVO] | None:
        return CarDAO.select_all_supplier_cars(self.connection, supplier_id)

    def insert_car(self, 
                   car: CarVO):
        command = InsertCar(car)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_car(self,
                   car: CarVO) -> None:
        command = DeleteCar(car)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_redo(command)


