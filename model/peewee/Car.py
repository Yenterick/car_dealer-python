from peewee import *

# Project imports
from model.peewee.BaseModel import BaseModel
from model.peewee.Supplier import Supplier

class Car(BaseModel):
    car_id = AutoField()
    model = CharField()
    year = IntegerField()
    type = CharField()
    
    supplier_id = ForeignKeyField(Supplier, backref='supplier_id')