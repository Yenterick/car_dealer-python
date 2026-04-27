from typing import List, Callable

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

from model.vo.EmployeeVO import EmployeeVO
from model.dao.EmployeeDAO import EmployeeDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.employee.InsertEmployee import InsertEmployee
from model.command.employee.DeleteEmployee import DeleteEmployee

from ui.consoleUtils import log

class EmployeeService:

    def __init__(self, 
                 connection_factory: Callable[[], Sqlite3Connection],
                 undo_manager: UndoRedoManager):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_employees(self) -> List[EmployeeVO]:
        with self.connection_factory() as connection:
            return EmployeeDAO.get_all_employees(connection)
    
    def get_employee(self, employee_id: int) -> EmployeeVO | None:
        with self.connection_factory() as connection:
            return EmployeeDAO.get_employee(connection, employee_id)

    def insert_employee(self, 
                        employee: EmployeeVO):
        command = InsertEmployee(employee)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.register(command)

    def delete_employee(self,
                        employee: EmployeeVO) -> None:
        command = DeleteEmployee(employee)

        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.register(command)


