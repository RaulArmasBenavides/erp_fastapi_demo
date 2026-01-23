from dependency_injector import containers, providers

from app.application.services import ItemService
from app.application.services.EntryService import EntryService
from app.core.models.config import configs
from app.infrastructure.repository import ItemRepository
from app.infrastructure.repository.EntryRepository import EntryRepository  
# from app.infrastructure.repository import *
from peewee import SqliteDatabase

from app.infrastructure.schema.entry_schema import EntrySchema
# def create_and_connect():
#         """Conecta a la base de datos y crea las tablas si no existen."""
#         db.connect()
#         db.create_tables([EntrySchema], safe=True)
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.entries",
            "app.core.dependencies",
        ]
    )

    #for sqlachemy
    #db = providers.Singleton(Database, db_url=configs.DATABASE_URI)
    #peewee
    # db = SqliteDatabase('entry.db')
    db = providers.Singleton(SqliteDatabase, 'entry.db')
    # db.connect()
    # db.create_tables([EntrySchema], safe=True)
    entry_repository = providers.Factory(EntryRepository,db=db)
    entry_service = providers.Factory(EntryService,entry_repository=entry_repository)
    item_repository =providers.Factory(ItemRepository,db=db)
    item_service = providers.Factory(ItemService,repo= item_repository)