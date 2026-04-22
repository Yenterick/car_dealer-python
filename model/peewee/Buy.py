from peewee import * # type: ignore

# Project imports
from model.peewee.BaseModel import BaseModel
from model.peewee.Supplier import Supplier
from model.peewee.Car import Car
from model.peewee.Spare import Spare

class Buy(BaseModel):
    buy_id = AutoField()
    cost = FloatField()

    supplier_id = ForeignKeyField(Supplier, backref='supplier_id')
    car_id = ForeignKeyField(Car, null=True, backref='car_id')
    spare_id = ForeignKeyField(Spare, null=True, backref='spare_id')

    