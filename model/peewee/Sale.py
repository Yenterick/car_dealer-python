from peewee import * # type: ignore

# Project imports
from model.peewee.BaseModel import BaseModel
from model.peewee.Car import Car
from model.peewee.Spare import Spare
from model.peewee.Customer import Customer
from model.peewee.Employee import Employee

class Sale(BaseModel):
    sale_id = IntegerField()
    value = FloatField()

    customer_id = ForeignKeyField(Customer, backref='customer_id')
    car_id = ForeignKeyField(Car, null=True, backref='car_id')
    spare_id = ForeignKeyField(Spare, backref='spare_id')
    employee_id = ForeignKeyField(Employee, backref='employee_id')