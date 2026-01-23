# app/presentation/routes/supplier_routes.py
from typing import List
from fastapi import APIRouter, Depends
from app.core.interfaces.i_supplier_service import ISupplierService
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.core.models.supplier import SupplierModel


router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)


@router.get("/", response_model=List[SupplierModel])
@inject
def get_suppliers(
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    return service.view_suppliers()


@router.post("/", response_model=SupplierModel)
@inject
def create_supplier(
    body: SupplierModel,
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    return service.add_supplier(body)


@router.delete("/{supplier_id}")
@inject
def delete_supplier(
    supplier_id: int,
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    service.delete_supplier(supplier_id)
    return {"message": "Supplier deleted"}
