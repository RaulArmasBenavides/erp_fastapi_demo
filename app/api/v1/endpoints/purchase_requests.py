# app/presentation/routes/purchase_request_routes.py
from typing import List

from fastapi import APIRouter, Depends
from app.core.interfaces.i_purchase_request_service import IPurchaseRequestService
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
 
from app.core.models.purchase_request import PurchaseRequestModel


router = APIRouter(
    prefix="/purchase-requests",
    tags=["purchase-requests"],
)


@router.get("/", response_model=List[PurchaseRequestModel])
@inject
def get_purchase_requests(
    supplier_id: int,
    service: IPurchaseRequestService = Depends(Provide[Container.purchase_request_service]),
):
    # Si pasas supplier_id, filtra; si no, lista todo
    return service.view_purchase_requests(supplier_id=supplier_id)


@router.post("/", response_model=PurchaseRequestModel)
@inject
def create_purchase_request(
    body: PurchaseRequestModel,
    service: IPurchaseRequestService = Depends(Provide[Container.purchase_request_service]),
):
    return service.add_purchase_request(body)


@router.delete("/{purchase_request_id}")
@inject
def delete_purchase_request(
    purchase_request_id: int,
    service: IPurchaseRequestService = Depends(Provide[Container.purchase_request_service]),
):
    service.delete_purchase_request(purchase_request_id)
    return {"message": "Purchase request deleted"}
