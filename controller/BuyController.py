from typing import List

# Project imports
from model.vo.BuyVO import BuyVO
from service.BuyService import BuyService

from ui.consoleUtils import log

class BuyController:

    def __init__(self, buy_service: BuyService):
        self.buy_service = buy_service

    def get_all_buys(self) -> List[BuyVO] | None:
        try:
            return self.buy_service.get_all_buys()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_buy(self, buy_id: int) -> BuyVO | None:
        try:
            return self.buy_service.get_buy(buy_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def select_all_supplier_buys(self, supplier_id: int) -> List[BuyVO] | None:
        try:
            return self.buy_service.select_all_supplier_buys(supplier_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_buy(self, cost: float, supplier, car=None, spare=None) -> None:
        try:
            buy = BuyVO(
                buy_id=None,
                cost=cost,
                supplier=supplier,
                car=car,
                spare=spare
            )
            self.buy_service.insert_buy(buy)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_buy(self, buy: BuyVO) -> None:
        try:
            self.buy_service.delete_buy(buy)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
