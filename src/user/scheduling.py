from peewee import *

db = SqliteDatabase('people.db')

class Task(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db
