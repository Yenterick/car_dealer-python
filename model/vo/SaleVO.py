from dataclasses import dataclass, field
from datetime import datetime

# Project imports
from model.vo.CarVO import CarVO
from model.vo.SpareVO import SpareVO
from model.vo.CustomerVO import CustomerVO
from model.vo.EmployeeVO import EmployeeVO

@dataclass
class SaleVO:
    sale_id: int
    customer: CustomerVO
    car: CarVO | None
    spare: SpareVO | None
    value: float
    employee: EmployeeVO | None
    created_at: datetime = field(default=datetime.now())
