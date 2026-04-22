from peewee import * # type: ignore

# Project imports
from model.peewee.BaseModel import BaseModel

class Supplier(BaseModel):
    supplier_id = AutoField()
    name = CharField()
    email = CharField()
    phone = CharField()


