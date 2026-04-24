from peewee import * # type: ignore
from datetime import datetime

db = SqliteDatabase("db/car_dealer.db")

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = db