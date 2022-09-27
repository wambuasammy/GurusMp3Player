"""creating database the database was created using mysqlite database"""
from peewee import *
from os import path
connection = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(connection,"mp3.db"))

class User(Model):
    name=CharField()
    email = CharField(unique=True)
    password = CharField()


    class Meta:
        database =db
User.create_table(fail_silently=True)
