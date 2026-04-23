# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.CarDAO import CarDAO
from model.vo.CarVO import CarVO

class DeleteCar(Command):

    def __init__(self,
                 car: CarVO):
        self.car = car
        self.car_id = None

    def redo(self, connection: Sqlite3Connection):
        self.car_id = self.car.car_id
        CarDAO.delete_car(self.car_id)

    def undo(self, connection: Sqlite3Connection):
        CarDAO.reinsert_car(
            connection,
            self.car
        )
