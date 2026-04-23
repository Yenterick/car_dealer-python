from typing import List

# Project imports
from model.vo.SpareVO import SpareVO
from service.SpareService import SpareService

from ui.consoleUtils import log

class SpareController:

    def __init__(self, spare_service: SpareService):
        self.spare_service = spare_service

    def get_all_spares(self) -> List[SpareVO] | None:
        try:
            return self.spare_service.get_all_spares()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_spare(self, spare_id: int) -> SpareVO | None:
        try:
            return self.spare_service.get_spare(spare_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def select_all_supplier_spares(self, supplier_id: int) -> List[SpareVO] | None:
        try:
            return self.spare_service.select_all_supplier_spares(supplier_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_spare(self, name: str, type: str, supplier) -> None:
        try:
            spare = SpareVO(
                spare_id=None,
                name=name,
                type=type,
                supplier=supplier
            )
            self.spare_service.insert_spare(spare)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_spare(self, spare: SpareVO) -> None:
        try:
            self.spare_service.delete_spare(spare)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
