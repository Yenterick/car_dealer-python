# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.CarDAO import CarDAO
from model.vo.CarVO import CarVO

class InsertCar(Command):

    def __init__(self,
                 car: CarVO):
        self.car = car
        self.car_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the car
        if self.car_id is None:
            self.car_id = CarDAO.insert_car(
                connection,
                self.car
            )
        else:
            # We're reinserting the car
            CarDAO.reinsert_car(
                connection,
                self.car
            )

    def undo(self, connection: Sqlite3Connection):
        CarDAO.delete_car(
            self.car_id
        )