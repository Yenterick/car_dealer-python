# Project imports
from typing import List

from model.vo.SupplierVO import SupplierVO
from service.SupplierService import SupplierService

from ui.consoleUtils import log

class SupplierControler:

    def __init__(self,
                 supplier_service: SupplierService):
        self.supplier_service = supplier_service

    def get_all_suppliers(self) -> List[SupplierVO] | None:
        try:
            return self.supplier_service.get_all_suppliers()
        except Exception as e:
            log(f"Error ocurred -> {str(e)}")

    
    

