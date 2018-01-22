from peewee import *
import os
import datetime
base_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = SqliteDatabase(base_dir + "/data.sqlite3")


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Schedule(BaseModel):
    date = DateTimeField(null=False)
    message = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)


DATABASE.create_tables([Schedule], safe=True)
