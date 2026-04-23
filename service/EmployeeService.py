from typing import List

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
                 connection: Sqlite3Connection,
                 undo_manager: UndoRedoManager):
        self.connection = connection
        self.undo_manager = undo_manager

    def get_all_employees(self) -> List[EmployeeVO]:
        return EmployeeDAO.get_all_employees()
    
    def get_employee(self, employee_id: int) -> EmployeeVO | None:
        return EmployeeDAO.get_employee(employee_id)

    def insert_employee(self, 
                        employee: EmployeeVO):
        command = InsertEmployee(employee)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.register(command)

    def delete_employee(self,
                        employee: EmployeeVO) -> None:
        command = DeleteEmployee(employee)

        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_redo(command)

    def undo(self) -> None:
        command = self.undo_manager.get_undo()
        if command is None:
            log("There's nothing to undo.")
            return
        
        with self.connection:
            command.undo(self.connection)

        self.undo_manager.push_redo(command)
        
    def redo(self) -> None:
        command = self.undo_manager.get_redo()
        if command is None:
            log("There's nothing to redo.")
            return
        
        with self.connection:
            command.redo(self.connection)

        self.undo_manager.push_undo(command)
