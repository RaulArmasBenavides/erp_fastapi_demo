# app/presentation/routes/supplier_routes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.api.security.roles import require_any_role
from app.application.services.supplier_service import SupplierService
from app.core.interfaces.i_supplier_service import ISupplierService
from app.domain.supplier import SupplierModel
from app.infrastructure.schema.user_schema import UserSchema
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
 


router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)


@router.get("/", response_model=List[SupplierModel])
@inject
def get_suppliers(
    user: UserSchema = Depends(require_any_role("Requester", "Approver")),
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    return service.view_suppliers()


# @router.post("/", response_model=SupplierModel)
# @inject
# def create_supplier(
#     body: SupplierModel,
#     user: UserSchema = Depends(require_any_role("Requester", "Approver")),
#     service: ISupplierService = Depends(Provide[Container.supplier_service]),
# ):
#     return service.add_supplier(body, created_by=user.email)


@router.post("/", response_model=SupplierModel)
@inject
async def create_supplier(
    name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    user: UserSchema = Depends(require_any_role("Requester", "Approver")),
    service: SupplierService = Depends(Provide[Container.supplier_service]),
):
    """
    Crea un nuevo proveedor con foto opcional
    """
    supplier_data = {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
    }

    return await service.create_supplier_with_photo(
        supplier_data=supplier_data, photo=photo, created_by=user.email
    )


@router.put("/{supplier_id}", response_model=SupplierModel)
@inject
async def update_supplier(
    supplier_id: int,
    name: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    user: UserSchema = Depends(require_any_role("Requester", "Approver")),
    service: SupplierService = Depends(Provide[Container.supplier_service]),
):
    """
    Actualiza un proveedor existente, incluyendo foto opcional
    """
    # Crear diccionario con los campos a actualizar (solo los que no son None)
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if address is not None:
        update_data["address"] = address
    if phone is not None:
        update_data["phone"] = phone
    if email is not None:
        update_data["email"] = email
    
    return await service.update_supplier_with_photo(
        supplier_id=supplier_id,
        update_data=update_data,
        photo=photo,
        updated_by=user.email
    )



@router.delete("/{supplier_id}")
@inject
def delete_supplier(
    supplier_id: int,
    user: UserSchema = Depends(require_any_role("Requester", "Approver")),
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    service.delete_supplier(supplier_id)
    return {"message": "Supplier deleted"}


@router.post("/{supplier_id}/approve", response_model=SupplierModel)
@inject
def approve_supplier(
    supplier_id: int,
    user: UserSchema = Depends(require_any_role("Approver")),
    service: ISupplierService = Depends(Provide[Container.supplier_service]),
):
    updated = service.approve_supplier(supplier_id, approved_by=user.email)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
        )

    return updated
