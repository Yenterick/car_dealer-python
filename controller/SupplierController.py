import re
from typing import List

# Project imports
from model.vo.SupplierVO import SupplierVO
from service.SupplierService import SupplierService

from ui.consoleUtils import log

class SupplierController:

    def __init__(self, supplier_service: SupplierService):
        self.supplier_service = supplier_service

    def get_all_suppliers(self) -> List[SupplierVO] | None:
        try:
            return self.supplier_service.get_all_suppliers()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_supplier(self, supplier_id: int) -> SupplierVO | None:
        try:
            return self.supplier_service.get_supplier(supplier_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_supplier(self, name: str, email: str, phone: str) -> None:
        try:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                raise ValueError(f"Invalid email format: {email}")

            supplier = SupplierVO(
                supplier_id=None,
                name=name,
                email=email,
                phone=phone
            )
            self.supplier_service.insert_supplier(supplier)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_supplier(self, supplier: SupplierVO) -> None:
        try:
            self.supplier_service.delete_supplier(supplier)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
