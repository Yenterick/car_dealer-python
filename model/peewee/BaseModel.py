from peewee import * # type: ignore
from datetime import datetime

db = SqliteDatabase("...")

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now())
    class Meta:
        database = db