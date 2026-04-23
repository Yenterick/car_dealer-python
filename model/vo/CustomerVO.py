from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CustomerVO:
    customer_id: int | None
    dni: str
    name: str
    last_name: str
    created_at: datetime = field(default=datetime.now())


    