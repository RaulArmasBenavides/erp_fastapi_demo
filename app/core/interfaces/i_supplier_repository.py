# app/core/interfaces/ISupplierRepository.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from app.domain.supplier import SupplierModel
 

class ISupplierRepository(ABC):
    @abstractmethod
    def add_supplier(
        self, supplier: SupplierModel, created_by: str
    ) -> SupplierModel: ...

    @abstractmethod
    def view_suppliers(self) -> List[SupplierModel]: ...

    @abstractmethod
    def delete_supplier(self, supplier_id: int) -> None: ...

    @abstractmethod
    def get_supplier(self, supplier_id: int) -> Optional[SupplierModel]:
        pass

    @abstractmethod
    def update_supplier(
        self, supplier_id: int, update_data: Dict[str, Any] 
    ) -> Optional[SupplierModel]:
        pass
