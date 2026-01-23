from typing import Any, Dict, List, Optional
from app.core.interfaces import IItemRepository
from peewee import Database

from app.core.models.item import Item
from app.infrastructure.schema.item_schema import ItemSchema

class ItemRepository(IItemRepository):
    """Repositorio de Items usando Peewee, con mapping genérico schema<->modelo."""
    def __init__(self, db: Database):
        self._db = db

    # ---------- Helpers ----------
    @staticmethod
    def _extract_schema_values(item: Item, *, exclude: set[str] | None = None) -> Dict[str, Any]:
        """Extrae del modelo solo los campos que existen en el Schema (evita KeyError)."""
        exclude = exclude or set()
        data: Dict[str, Any] = {}
        schema_fields = ItemSchema._meta.fields.keys()
        for name in schema_fields:
            if name in exclude:
                continue
            if hasattr(item, name):
                data[name] = getattr(item, name)
        return data

    @staticmethod
    def _to_model(row: ItemSchema) -> Item:
        """Convierte un registro Peewee al modelo Pydantic/DTO."""
        # Asume que los nombres de campos entre schema y modelo coinciden.
        # Si usas Pydantic v1:
        return Item(**row.__data__)
        # Si prefieres ser más explícito, mapea campo por campo aquí.

    # ---------- CRUD ----------
    def add_item(self, item: Item) -> Item:
        with self._db.atomic():
            data = self._extract_schema_values(item, exclude={"id"})
            rec = ItemSchema.create(**data)
            return self._to_model(rec)

    def view_items(self) -> List[Item]:
        return [self._to_model(r) for r in ItemSchema.select()]

    def get_item(self, item_id: int) -> Optional[Item]:
        try:
            rec = ItemSchema.get(ItemSchema.id == item_id)
            return self._to_model(rec)
        except ItemSchema.DoesNotExist:
            return None

    def update_item(self, item_id: int, item: Item) -> Optional[Item]:
        with self._db.atomic():
            try:
                rec = ItemSchema.get(ItemSchema.id == item_id)
            except ItemSchema.DoesNotExist:
                return None

            data = self._extract_schema_values(item, exclude={"id"})
            for k, v in data.items():
                setattr(rec, k, v)
            rec.save()  # guarda solo lo modificado
            return self._to_model(rec)

    def delete_item(self, item_id: int) -> bool:
        with self._db.atomic():
            deleted = ItemSchema.delete().where(ItemSchema.id == item_id).execute()
            return bool(deleted)