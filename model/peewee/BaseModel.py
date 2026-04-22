from peewee import *
from datetime import datetime

db = SqliteDatabase("...")

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now())

    @classmethod
    def select_all(cls):
        return cls.select()
    
    @classmethod
    def select_by_id(cls, id: int):
        return cls.get_by_id(id)

    class Meta:
        database = db