from typing import Optional, List
from sqlite3 import Cursor

# Project imports
from db.Sqlite3Connection import Sqlite3Connection

# Manual VOs
from model.vo.SaleVO import SaleVO
from model.vo.EmployeeVO import EmployeeVO
from model.vo.CustomerVO import CustomerVO
from model.vo.CarVO import CarVO
from model.vo.SpareVO import SpareVO
from model.vo.SupplierVO import SupplierVO

# Peewee VOs
from model.peewee.Sale import Sale

class SaleDAO:

    @staticmethod
    def get_all_sales() -> List[Sale]:
        return Sale.select()
    
    @staticmethod
    def get_sale(id: int) -> Sale:
        return Sale.get_by_id(id)
    
    @staticmethod
    def delete_sale(id: int) -> None:
        Sale.delete_by_id(id)

    @staticmethod
    def insert_sale(connection: Sqlite3Connection,
                    sale: SaleVO,
                    customer_id: int,
                    car_id: Optional[int],
                    spare_id: Optional[int],
                    employee_id: int) -> int | None:
  
        query_string: str = 'INSERT INTO sale (value, customer_id, car_id, spare_id, employee_id) VALUES (?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (
                                                sale.value,
                                                customer_id,
                                                car_id,
                                                spare_id,
                                                employee_id
                                           ))
        
        sale_id = cursor.lastrowid
        return sale_id
    
    @staticmethod
    def reinsert_sale(connection: Sqlite3Connection,
                      sale: SaleVO,
                      customer_id: int,
                      car_id: Optional[int],
                      spare_id: Optional[int],
                      employee_id: int) -> int | None:
  
        query_string: str = 'INSERT INTO sale (sale_id, value, customer_id, car_id, spare_id, employee_id) VALUES (?, ?, ?, ?, ?, ?)'

        cursor: Cursor = connection.execute(query_string,
                                           (    
                                                sale.sale_id,
                                                sale.value,
                                                customer_id,
                                                car_id,
                                                spare_id,
                                                employee_id
                                           ))
        
        sale_id = cursor.lastrowid
        return sale_id

    @staticmethod
    def select_all_employee_sales(connection: Sqlite3Connection,
                                  employee_id: int) -> List[SaleVO] | None:
        
        query_string: str = '''
            SELECT  s.sale_id,
                    s.value,
                    e.employee_id,
                    e.dni as employee_dni,
                    e.name as employee_name,
                    e.last_name as employee_last_name,
                    cu.customer_id,
                    cu.dni as customer_dni,
                    cu.name as customer_name,
                    cu.last_name as customer_last_name,
                    c.car_id,
                    c.model,
                    c.year,
                    c.type as car_type,
                    sp.spare_id,
                    sp.name as spare_name,
                    sp.type as spare_type,
                    sup_c.supplier_id as car_supplier_id,
                    sup_c.name as car_supplier_name,
                    sup_c.email as car_supplier_email,
                    sup_c.phone as car_supplier_phone,
                    sup_sp.supplier_id as spare_supplier_id,
                    sup_sp.name as spare_supplier_name,
                    sup_sp.email as spare_supplier_email,
                    sup_sp.phone as spare_supplier_phone
            FROM sale s
            JOIN employee e ON s.employee_id = e.employee_id
            JOIN customer cu ON s.customer_id = cu.customer_id
            LEFT JOIN car c ON s.car_id = c.car_id
            LEFT JOIN spare sp ON s.spare_id = sp.spare_id
            LEFT JOIN supplier sup_c ON c.supplier_id = sup_c.supplier_id
            LEFT JOIN supplier sup_sp ON sp.supplier_id = sup_sp.supplier_id
            WHERE e.employee_id = ?
            '''
        
        cursor: Cursor = connection.execute(query_string,
                                            (
                                                employee_id
                                            ))
        
        employee_sales: List[SaleVO] = []

        for registry in cursor:

            loaded_registry: dict = dict(registry)

            employee: EmployeeVO = EmployeeVO(
                employee_id=loaded_registry['employee_id'],
                dni=loaded_registry['employee_dni'],
                name=loaded_registry['employee_name'],
                last_name=loaded_registry['employee_last_name']
            )

            customer: CustomerVO = CustomerVO(
                customer_id=loaded_registry['customer_id'],
                dni=loaded_registry['customer_dni'],
                name=loaded_registry['customer_name'],
                last_name=loaded_registry['customer_last_name']
            )

            car: CarVO | None = None
            if loaded_registry['car_id'] is not None:
                car_supplier: SupplierVO = SupplierVO(
                    supplier_id=loaded_registry['car_supplier_id'],
                    name=loaded_registry['car_supplier_name'],
                    email=loaded_registry['car_supplier_email'],
                    phone=loaded_registry['car_supplier_phone']
                )
                car = CarVO(
                    car_id=loaded_registry['car_id'],
                    model=loaded_registry['model'],
                    year=loaded_registry['year'],
                    type=loaded_registry['car_type'],
                    supplier=car_supplier
                )
            
            spare: SpareVO | None = None
            if loaded_registry['spare_id'] is not None:
                spare_supplier: SupplierVO = SupplierVO(
                    supplier_id=loaded_registry['spare_supplier_id'],
                    name=loaded_registry['spare_supplier_name'],
                    email=loaded_registry['spare_supplier_email'],
                    phone=loaded_registry['spare_supplier_phone']
                )
                spare = SpareVO(
                    spare_id=loaded_registry['spare_id'],
                    name=loaded_registry['spare_name'],
                    type=loaded_registry['spare_type'],
                    supplier=spare_supplier
                )

            sale: SaleVO = SaleVO(
                sale_id=loaded_registry['sale_id'],
                customer=customer,
                car=car,
                spare=spare,
                value=loaded_registry['value'],
                employee=employee
            )

            employee_sales.append(sale)

        return employee_sales
