from typing import List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.EmployeeVO import EmployeeVO

# Peewee VOs
from model.peewee.Employee import Employee

# DAOs for lazy loading
from model.dao.SaleDAO import SaleDAO

class EmployeeDAO:

    @staticmethod
    def get_all_employees(connection: Sqlite3Connection) -> List[EmployeeVO]:
        peewee_employees = Employee.select()
        employees = []
        for peewee_employee in peewee_employees:
            employee = EmployeeVO(
                employee_id=peewee_employee.employee_id,
                dni=peewee_employee.dni,
                name=peewee_employee.name,
                last_name=peewee_employee.last_name
            )

            employee._sales_loader = lambda f=connection, e_id=peewee_employee.employee_id: SaleDAO.select_all_employee_sales(f, e_id)
            employees.append(employee)
        return employees
    
    @staticmethod
    def get_employee(connection: Sqlite3Connection, id: int) -> EmployeeVO | None:
        peewee_employee = Employee.get_or_none(id)
        
        if peewee_employee is None:
            return None

        return EmployeeVO(
            employee_id=peewee_employee.employee_id,
            dni=peewee_employee.dni,
            name=peewee_employee.name,
            last_name=peewee_employee.last_name,
            _sales_loader=lambda: SaleDAO.select_all_employee_sales(connection, peewee_employee.employee_id)
        )
    
    @staticmethod
    def delete_employee(id: int | None) -> None:
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
