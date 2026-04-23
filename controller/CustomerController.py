from typing import List

# Project imports
from model.vo.CustomerVO import CustomerVO
from service.CustomerService import CustomerService

from ui.consoleUtils import log

class CustomerController:

    def __init__(self, customer_service: CustomerService):
        self.customer_service = customer_service

    def get_all_customers(self) -> List[CustomerVO] | None:
        try:
            return self.customer_service.get_all_customers()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_customer(self, customer_id: int) -> CustomerVO | None:
        try:
            return self.customer_service.get_customer(customer_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_customer(self, dni: str, name: str, last_name: str) -> None:
        try:
            customer = CustomerVO(
                customer_id=None,
                dni=dni,
                name=name,
                last_name=last_name
            )
            self.customer_service.insert_customer(customer)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_customer(self, customer: CustomerVO) -> None:
        try:
            self.customer_service.delete_customer(customer)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
