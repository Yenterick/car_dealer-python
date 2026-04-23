from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SupplierVO:
    supplier_id: int | None
    name: str
    email: str
    phone: str
    created_at: datetime = field(default=datetime.now())