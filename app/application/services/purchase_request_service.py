# app/application/services/purchase_request_service.py
from typing import List, Optional

from app.application.services.base_service import BaseService
from app.core.interfaces.i_purchase_request_repository import IPurchaseRequestRepository
from app.core.interfaces.i_purchase_request_service import IPurchaseRequestService

from app.core.models.purchase_request import PurchaseRequestModel


class PurchaseRequestService(BaseService, IPurchaseRequestService):
    def __init__(self, purchase_request_repository: IPurchaseRequestRepository):
        self._repo = purchase_request_repository

    def add_purchase_request(self, pr: PurchaseRequestModel) -> PurchaseRequestModel:
        return self._repo.add_purchase_request(pr)

    def view_purchase_requests(
        self, supplier_id: Optional[int] = None
    ) -> List[PurchaseRequestModel]:
        # Si supplier_id viene, filtra; si no, lista todo
        if supplier_id is None:
            return self._repo.view_purchase_requests()

        return self._repo.view_purchase_requests_by_supplier(supplier_id)

    def delete_purchase_request(self, purchase_request_id: int) -> None:
        self._repo.delete_purchase_request(purchase_request_id)
