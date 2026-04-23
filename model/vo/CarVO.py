from dataclasses import dataclass, field
from datetime import datetime

# Project imports
from model.vo.SupplierVO import SupplierVO

@dataclass
class CarVO:
    car_id: int | None
    model: str
    year: int
    type: str
    supplier: SupplierVO
    created_at: datetime = field(default=datetime.now())