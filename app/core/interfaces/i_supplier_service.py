from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.models.supplier import SupplierModel


class ISupplierService(ABC):
    @abstractmethod
    def add_supplier(self, supplier: SupplierModel) -> SupplierModel: ...

    @abstractmethod
    def view_suppliers(self) -> List[SupplierModel]: ...

    @abstractmethod
    def delete_supplier(self, supplier_id: int) -> None: ...
    
    @abstractmethod
    def approve_supplier(self, supplier_id: int, approved_by: str) -> Optional[SupplierModel]:
        pass