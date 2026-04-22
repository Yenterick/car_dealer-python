from peewee import *

# Project imports
from model.peewee.BaseModel import BaseModel

class Employee(BaseModel):
    employee_id = AutoField()
    dni = CharField()
    name = CharField()
    last_name = CharField()
