# app/core/interfaces/i_purchase_request_repository.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.core.models.purchase_request import PurchaseRequestModel


class IPurchaseRequestRepository(ABC):
    @abstractmethod
    def add_purchase_request(self, pr: PurchaseRequestModel) -> PurchaseRequestModel:
        ...

    @abstractmethod
    def view_purchase_requests(self) -> List[PurchaseRequestModel]:
        ...

    @abstractmethod
    def view_purchase_requests_by_supplier(self, supplier_id: int) -> List[PurchaseRequestModel]:
        ...

    @abstractmethod
    def delete_purchase_request(self, purchase_request_id: int) -> None:
        ...
