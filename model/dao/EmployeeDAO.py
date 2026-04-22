from typing import Optional, List
from sqlite3 import Cursor, Connection

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.EmployeeVO import EmployeeVO

# Peewee VOs
from model.peewee.Employee import Employee

class EmployeeDAO:

    @staticmethod
    def get_all_employees() -> List[Employee]:
        return Employee.select()
    
    @staticmethod
    def get_employee(id: int) -> Employee:
        return Employee.get_by_id(id)
    
    @staticmethod
    def delete_employee(id: int) -> None:
        Employee.delete_by_id(id)
