from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EmployeeVO:
    employee_id: int
    dni: str
    name: str
    last_name: str
    created_at: datetime = field(default=datetime.now())


    