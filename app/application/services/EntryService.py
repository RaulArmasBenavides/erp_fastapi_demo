from typing import List
from app.application.services.base_service import BaseService
from app.core.interfaces.IEntryRepository import IEntryRepository
from app.core.interfaces.IEntryService import IEntryService
from app.core.models.entry import EntryModel

class EntryService(BaseService, IEntryService):
    def __init__(self, entry_repository: IEntryRepository):
        self._entry_repository = entry_repository

    def add_entry(self, entry: EntryModel) -> EntryModel:
        return self._entry_repository.add_entry(entry)

    def view_entries(self) -> List[EntryModel]:
        return self._entry_repository.view_entries()

    def delete_entry(self, entry_id: int) -> None:
        self._entry_repository.delete_entry(entry_id)