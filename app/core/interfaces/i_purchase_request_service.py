# app/core/interfaces/i_purchase_request_service.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.purchase_request import PurchaseRequestModel

 

class IPurchaseRequestService(ABC):
    @abstractmethod
    def add_purchase_request(self, pr: PurchaseRequestModel) -> PurchaseRequestModel:
        ...

    @abstractmethod
    def view_purchase_requests(self, supplier_id: Optional[int] = None) -> List[PurchaseRequestModel]:
        ...

    @abstractmethod
    def delete_purchase_request(self, purchase_request_id: int) -> None:
        ...
