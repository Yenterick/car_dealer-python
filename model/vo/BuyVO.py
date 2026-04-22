from dataclasses import dataclass, field
from datetime import datetime

# Project imports
from model.vo.SupplierVO import SupplierVO
from model.vo.CarVO import CarVO
from model.vo.SpareVO import SpareVO

@dataclass
class BuyVO:
    buy_id: int
    supplier: SupplierVO
    car: CarVO | None
    spare: SpareVO | None
    cost: float
    created_at: datetime = field(default=datetime.now())

    