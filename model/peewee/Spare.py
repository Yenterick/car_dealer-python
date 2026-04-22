from peewee import *

# Project imports
from model.peewee.BaseModel import BaseModel
from model.peewee.Supplier import Supplier

class Spare(BaseModel):
    spare_id = AutoField()
    name = CharField()
    type = CharField()
    
    supplier_id = ForeignKeyField(Supplier, backref='supplier_id')