from peewee import Model,TextField 
from .db import db_proxy

class ItemSchema(Model):
    name = TextField()
    description = TextField()

    class Meta: 
        database = db_proxy
