from typing import List, Optional
from app.core.exceptions import NotFoundError
from app.application.services.base_service import BaseService
from app.core.interfaces import IItemRepository
from app.core.interfaces.i_item_service import IItemService
from app.core.models.item import Item

class ItemService(BaseService, IItemService):
    """Orquestador de casos de uso para Items (sync)."""

    def __init__(self, repo: IItemRepository):
        self._repo = repo
        if hasattr(self, "logger"):
            self.logger.debug("ItemService inicializado")

    def create(self, item: Item) -> Item:
        """Crea un item."""
        return self._repo.add(item)

    def list(self) -> List[Item]:
        """Lista todos los items."""
        return self._repo.get_all()

    def update(self, item_id: int, item: Item) -> Item:
        """Reemplaza un item existente por id."""
        updated: Optional[Item] = self._repo.replace(item_id, item)
        if updated is None:
            raise NotFoundError(f"Item {item_id} no existe")
        return updated

    def delete(self, item_id: int) -> None:
        """Elimina un item por id."""
        ok: bool = self._repo.remove(item_id)
        if not ok:
            raise NotFoundError(f"Item {item_id} no existe")