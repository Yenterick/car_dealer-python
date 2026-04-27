from peewee import * # type: ignore

# Project imports
from model.peewee.BaseModel import BaseModel
from model.peewee.Car import Car
from model.peewee.Spare import Spare
from model.peewee.Customer import Customer
from model.peewee.Employee import Employee

class Sale(BaseModel):
    sale_id = AutoField()
    value = FloatField()

    customer_id = ForeignKeyField(Customer, column_name='customer_id', backref='customer_id')
    car_id = ForeignKeyField(Car, null=True, column_name='car_id', backref='car_id')
    spare_id = ForeignKeyField(Spare, null=True, column_name='spare_id', backref='spare_id')
    employee_id = ForeignKeyField(Employee, column_name='employee_id', backref='employee_id')