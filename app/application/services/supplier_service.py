from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from app.application.services.base_service import BaseService

from app.application.services.cloudinary_service import CloudinaryService
from app.core.interfaces.i_supplier_repository import ISupplierRepository
from app.core.interfaces.i_supplier_service import ISupplierService
from app.core.models.supplier import SupplierModel
from app.infrastructure.schema.supplier_schema import SupplierSchema


class SupplierService(BaseService, ISupplierService):
    def __init__(self, supplier_repository: ISupplierRepository):
        self._supplier_repository = supplier_repository
        self._cloudinary_service = CloudinaryService()

    def add_supplier(self, supplier: SupplierModel, created_by: str) -> SupplierModel:
        return self._supplier_repository.add_supplier(supplier, created_by)

    def view_suppliers(self) -> List[SupplierModel]:
        return self._supplier_repository.view_suppliers()

    def approve_supplier(
        self, supplier_id: int, approved_by: str
    ) -> Optional[SupplierModel]:
        return self._supplier_repository.approve_supplier(supplier_id, approved_by)

    def delete_supplier(self, supplier_id: int) -> None:
        self._supplier_repository.delete_supplier(supplier_id)

    async def create_supplier_with_photo(
        self, supplier_data: dict, photo: Optional[UploadFile], created_by: str
    ) -> SupplierModel:

        # Subir foto a Cloudinary si se proporciona
        photo_url = None
        photo_public_id = None

        if photo and photo.content_type.startswith("image/"):
            try:
                upload_result = await self._cloudinary_service.upload_image(
                    photo, folder="suppliers"
                )
                photo_url = upload_result.get("secure_url")
                photo_public_id = upload_result.get("public_id")
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error al subir la foto: {str(e)}"
                )

        # Crear objeto SupplierModel
        supplier = SupplierModel(
            **supplier_data,
            photo=photo_url,
            photo_public_id=photo_public_id,
            created_by=created_by,
            is_approved=False,
        )

        return self.add_supplier(supplier, created_by)

    async def update_supplier_with_photo(
        self,
        supplier_id: int,
        update_data: dict,
        photo: Optional[UploadFile] = None,
        updated_by: str = None,
    ) -> Optional[SupplierModel]:
        """
        Actualiza un proveedor, opcionalmente con nueva foto.
        Permite actualizar otros campos aunque no se cargue una foto.
        """
        # Obtener proveedor actual
        current_supplier = self._supplier_repository.get_supplier(supplier_id)
        if not current_supplier:
            return None

        # Manejar foto nueva si se proporciona
        if photo is not None:
            if (
                photo.filename
                and photo.content_type
                and photo.content_type.startswith("image/")
            ):
                # Eliminar foto anterior si existe
                if current_supplier.photo:
                    await self._cloudinary_service.delete_resource(
                        current_supplier.photo
                    )

                # Subir nueva foto
                try:
                    upload_result = await self._cloudinary_service.upload_image(
                        photo, folder="suppliers"
                    )
                    update_data["photo"] = upload_result.get("secure_url")
                    update_data["photo_public_id"] = upload_result.get("public_id")
                except Exception as e:
                    raise HTTPException(
                        status_code=400, detail=f"Error al subir la foto: {str(e)}"
                    )
            elif photo.filename:  # Se envió un archivo pero no es imagen
                raise HTTPException(
                    status_code=400, detail="El archivo subido no es una imagen válida"
                )
            # Si photo.filename está vacío (se envió un campo File vacío), simplemente no se hace nada con la foto

        # Agregar información del usuario que actualiza
        if updated_by:
            update_data["updated_by"] = updated_by
            update_data["updated_at"] = datetime.utcnow()

        # Actualizar proveedor con los datos (pueden incluir solo campos no relacionados con la foto)
        return self._supplier_repository.update_supplier(supplier_id, update_data)

    def get_supplier(self, supplier_id: int) -> Optional[SupplierModel]:
        supplier = (
            self.session.query(SupplierSchema)
            .filter(SupplierSchema.id == supplier_id)
            .first()
        )

        if supplier:
            return SupplierModel.from_orm(supplier)
        return None
