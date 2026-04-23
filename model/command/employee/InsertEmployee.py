# Project imports
from model.command.Command import Command

from db.Sqlite3Connection import Sqlite3Connection

from model.dao.EmployeeDAO import EmployeeDAO
from model.vo.EmployeeVO import EmployeeVO

class InsertEmployee(Command):

    def __init__(self,
                 employee: EmployeeVO):
        self.employee = employee
        self.employee_id = None

    def redo(self, connection: Sqlite3Connection):
        # Validating if is the first time we're adding the employee
        if self.employee_id is None:
            self.employee_id = EmployeeDAO.insert_employee(
                connection,
                self.employee
            )
        else:
            # We're reinserting the employee
            EmployeeDAO.reinsert_employee(
                connection,
                self.employee
            )

    def undo(self, connection: Sqlite3Connection):
        EmployeeDAO.delete_employee(
            self.employee_id
        )
