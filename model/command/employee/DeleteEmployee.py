# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.EmployeeDAO import EmployeeDAO
from model.vo.EmployeeVO import EmployeeVO

class DeleteEmployee(Command):

    def __init__(self,
                 employee: EmployeeVO):
        self.employee = employee
        self.employee_id = None

    def redo(self, connection: Sqlite3Connection):
        self.employee_id = self.employee.employee_id
        EmployeeDAO.delete_employee(self.employee_id)

    def undo(self, connection: Sqlite3Connection):
        EmployeeDAO.reinsert_employee(
            connection,
            self.employee
        )
