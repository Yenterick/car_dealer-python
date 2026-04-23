from dataclasses import dataclass, field
from datetime import datetime

# Project imports
from model.vo.SupplierVO import SupplierVO

@dataclass
class SpareVO:
    spare_id: int | None
    name: str
    type: str
    supplier: SupplierVO
    created_at: datetime = field(default=datetime.now())