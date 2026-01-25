from typing import List, Optional
from app.application.services.base_service import BaseService

from app.core.interfaces.i_supplier_repository import ISupplierRepository
from app.core.interfaces.i_supplier_service import ISupplierService
from app.core.models.supplier import SupplierModel


class SupplierService(BaseService, ISupplierService):
    def __init__(self, supplier_repository: ISupplierRepository):
        self._supplier_repository = supplier_repository

    def add_supplier(self, supplier: SupplierModel,created_by: str) -> SupplierModel:
        return self._supplier_repository.add_supplier(supplier,created_by)

    def view_suppliers(self) -> List[SupplierModel]:
        return self._supplier_repository.view_suppliers()

    def approve_supplier(
        self, supplier_id: int, approved_by: str
    ) -> Optional[SupplierModel]:
        return self._supplier_repository.approve_supplier(supplier_id, approved_by)

    def delete_supplier(self, supplier_id: int) -> None:
        self._supplier_repository.delete_supplier(supplier_id)
