# app/core/interfaces/ISupplierRepository.py
from abc import ABC, abstractmethod
from typing import List
from app.core.models.supplier import SupplierModel


class ISupplierRepository(ABC):
    @abstractmethod
    def add_supplier(self, supplier: SupplierModel) -> SupplierModel: ...

    @abstractmethod
    def view_suppliers(self) -> List[SupplierModel]: ...

    @abstractmethod
    def delete_supplier(self, supplier_id: int) -> None: ...
