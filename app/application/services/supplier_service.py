from typing import List, Optional

from fastapi import HTTPException, UploadFile
from app.application.services.base_service import BaseService

from app.application.services.cloudinary_service import CloudinaryService
from app.core.interfaces.i_supplier_repository import ISupplierRepository
from app.core.interfaces.i_supplier_service import ISupplierService
from app.core.models.supplier import SupplierModel


class SupplierService(BaseService, ISupplierService):
    def __init__(self, supplier_repository: ISupplierRepository):
        self._supplier_repository = supplier_repository
        self._cloudinary_service = CloudinaryService()

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
        
    async def create_supplier_with_photo(
        self, 
        supplier_data: dict, 
        photo: Optional[UploadFile],
        created_by: str
    ) -> SupplierModel:
       
        # Subir foto a Cloudinary si se proporciona
        photo_url = None
        photo_public_id = None
        
        if photo and photo.content_type.startswith('image/'):
            try:
                upload_result = await self._cloudinary_service.upload_image(
                    photo,
                    folder="suppliers"
                )
                photo_url = upload_result.get("secure_url")
                photo_public_id = upload_result.get("public_id")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al subir la foto: {str(e)}"
                )
        
        # Crear objeto SupplierModel
        supplier = SupplierModel(
            **supplier_data,
            photo=photo_url,
            photo_public_id=photo_public_id,
            created_by=created_by,
            is_approved=False
        )
        
        return self.add_supplier(supplier, created_by)

    async def update_supplier_with_photo(
        self, 
        supplier_id: int, 
        update_data: dict, 
        photo: Optional[UploadFile],
        updated_by: str
    ) -> Optional[SupplierModel]:
        """
        Actualiza un proveedor, opcionalmente con nueva foto
        """
        # Obtener proveedor actual
        current_supplier = self.get_supplier(supplier_id)
        if not current_supplier:
            return None
        
        # Manejar foto nueva
        if photo and photo.content_type.startswith('image/'):
            # Eliminar foto anterior si existe
            if current_supplier.photo_public_id:
                await self._cloudinary_service.delete_resource(current_supplier.photo_public_id)
            
            # Subir nueva foto
            try:
                upload_result = await self._cloudinary_service.upload_image(
                    photo,
                    folder="suppliers"
                )
                update_data["photo_url"] = upload_result.get("secure_url")
                update_data["photo_public_id"] = upload_result.get("public_id")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al subir la foto: {str(e)}"
                )
        
        # Actualizar proveedor
        return self._supplier_repository.update_supplier(supplier_id, update_data)

