from typing import List

# Project imports
from model.vo.SaleVO import SaleVO
from service.SaleService import SaleService

from ui.consoleUtils import log

class SaleController:

    def __init__(self, sale_service: SaleService):
        self.sale_service = sale_service

    def get_all_sales(self) -> List[SaleVO] | None:
        try:
            return self.sale_service.get_all_sales()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_sale(self, sale_id: int) -> SaleVO | None:
        try:
            return self.sale_service.get_sale(sale_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def select_all_employee_sales(self, employee_id: int) -> List[SaleVO] | None:
        try:
            return self.sale_service.select_all_employee_sales(employee_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_sale(self, value: float, customer, employee, car=None, spare=None) -> None:
        try:
            sale = SaleVO(
                sale_id=None,
                value=value,
                customer=customer,
                employee=employee,
                car=car,
                spare=spare
            )
            self.sale_service.insert_sale(sale)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_sale(self, sale: SaleVO) -> None:
        try:
            self.sale_service.delete_sale(sale)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
