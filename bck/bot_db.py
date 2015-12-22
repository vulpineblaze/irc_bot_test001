
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')
db.connect()




class BaseModel(Model):
    class Meta:
        database = db

class Admin(BaseModel):
    version = CharField(unique=True, default="1.1.0")
    is_debug = BooleanField(default=True)

class Profile(BaseModel):
    alt_username = CharField(default="Player", unique=True)
    does_attack  = CharField(default="attacks")
    does_defend = CharField(default="defends")
    does_crit = CharField(default="crits")
    does_heal = CharField(default="heals")
    does_rez = CharField(default="rez's")
    damage = CharField(default="damage")
    if_die_msg = CharField(default="dies")
    attack = CharField(default="attack")
    defense = CharField(default="defense")
    crit = CharField(default="crit")
    level = CharField(default="level")
    juice = CharField(default="juice")
    health = CharField(default="health")


class User(BaseModel):
    username = CharField(unique=True)
    profile = Profile()
    attack = IntegerField(default=1)
    defense = IntegerField(default=1)
    crit = IntegerField(default=1)
    level = IntegerField(default=1)
    juice = IntegerField(default=1)
    health = IntegerField(default=1)
    is_active = BooleanField(default=True)
    last_rez = DateTimeField()
    finish_training = DateTimeField()

        

# class Tweet(BaseModel):
#     user = ForeignKeyField(User, related_name='tweets')
#     message = TextField()
#     created_date = DateTimeField(default=datetime.datetime.now)
#     is_published = BooleanField(default=True)


# class Monster(BaseModel):
#     # user = ForeignKeyField(User, related_name='tweets')
#     message = CharField(default="basic baddie")
#     created_date = DateTimeField(default=datetime.datetime.now)
#     is_alive = BooleanField(default=True)
#     attack = IntegerField(default=1)
#     defense = IntegerField(default=1)
#     health = IntegerField(default=100)




db.create_tables([User, Admin], safe=True)