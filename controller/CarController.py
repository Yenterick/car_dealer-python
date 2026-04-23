from typing import List

# Project imports
from model.vo.CarVO import CarVO
from service.CarService import CarService

from ui.consoleUtils import log

class CarController:

    def __init__(self, car_service: CarService):
        self.car_service = car_service

    def get_all_cars(self) -> List[CarVO] | None:
        try:
            return self.car_service.get_all_cars()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_car(self, car_id: int) -> CarVO | None:
        try:
            return self.car_service.get_car(car_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def select_all_supplier_cars(self, supplier_id: int) -> List[CarVO] | None:
        try:
            return self.car_service.select_all_supplier_cars(supplier_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_car(self, model: str, year: int, type: str, supplier) -> None:
        try:
            car = CarVO(
                car_id=None,
                model=model,
                year=year,
                type=type,
                supplier=supplier
            )
            self.car_service.insert_car(car)
            log("Car inserted correctly.")
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_car(self, car: CarVO) -> None:
        try:
            self.car_service.delete_car(car)
            log("Car deleted correctly.")
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
