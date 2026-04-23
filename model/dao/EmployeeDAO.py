from typing import Optional, List
from sqlite3 import Cursor

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

    @staticmethod
    def insert_employee(connection: Sqlite3Connection,
                        employee: EmployeeVO) -> int | None:
  
        query_string: str = 'INSERT INTO employee (dni, name, last_name) VALUES (?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                employee.dni,
                                                employee.name,
                                                employee.last_name
                                           ))
        
        employee_id = cursor.lastrowid
        return employee_id
    
    @staticmethod
    def reinsert_employee(connection: Sqlite3Connection,
                          employee: EmployeeVO) -> int | None:

        query_string: str = 'INSERT INTO employee (employee_id, dni, name, last_name) VALUES (?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                employee.employee_id,
                                                employee.dni,
                                                employee.name,
                                                employee.last_name
                                           ))
        
        employee_id = cursor.lastrowid
        return employee_id
