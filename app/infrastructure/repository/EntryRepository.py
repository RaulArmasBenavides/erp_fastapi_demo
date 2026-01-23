import datetime
from typing import List
from collections import OrderedDict
from app.core.interfaces.IEntryRepository import IEntryRepository
from app.core.models.entry import EntryModel
from app.infrastructure.schema.entry_schema import EntrySchema
from peewee import SqliteDatabase,Database
class EntryRepository( IEntryRepository):
     
     def __init__(self, db: Database):
        self._db = db
    

     def add_entry(self, entry: EntryModel) -> EntryModel:
         with self._db.atomic():
             peewee_model = EntrySchema.create(content=entry.content)
             return EntryModel(id=peewee_model.id, content=peewee_model.content, timestamp=peewee_model.timestamp)

     def view_entries(self) -> List[EntryModel]:
         entries = EntrySchema.select()
         return [EntryModel(id=e.id, content=e.content, timestamp=e.timestamp) for e in entries]

     def delete_entry(self, entry_id: int) -> None:
         entry = EntrySchema.get(EntrySchema.id == entry_id)
         entry.delete_instance()


