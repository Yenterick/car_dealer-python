from typing import List

# Project imports
from model.vo.EmployeeVO import EmployeeVO
from service.EmployeeService import EmployeeService

from ui.consoleUtils import log

class EmployeeController:

    def __init__(self, employee_service: EmployeeService):
        self.employee_service = employee_service

    def get_all_employees(self) -> List[EmployeeVO] | None:
        try:
            return self.employee_service.get_all_employees()
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def get_employee(self, employee_id: int) -> EmployeeVO | None:
        try:
            return self.employee_service.get_employee(employee_id)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def insert_employee(self, dni: str, name: str, last_name: str) -> None:
        try:
            employee = EmployeeVO(
                employee_id=None,
                dni=dni,
                name=name,
                last_name=last_name
            )
            self.employee_service.insert_employee(employee)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")

    def delete_employee(self, employee: EmployeeVO) -> None:
        try:
            self.employee_service.delete_employee(employee)
        except Exception as e:
            log(f"Error occurred -> {str(e)}")
