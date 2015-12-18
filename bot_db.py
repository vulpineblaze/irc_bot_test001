
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')
db.connect()




class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    attack = IntegerField(default=1)
    defense = IntegerField(default=1)
    health = IntegerField(default=100)

class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


class Monster(BaseModel):
    # user = ForeignKeyField(User, related_name='tweets')
    message = CharField(default="basic baddie")
    created_date = DateTimeField(default=datetime.datetime.now)
    is_alive = BooleanField(default=True)
    attack = IntegerField(default=1)
    defense = IntegerField(default=1)
    health = IntegerField(default=100)




db.create_tables([User, Tweet, Monster], safe=True)