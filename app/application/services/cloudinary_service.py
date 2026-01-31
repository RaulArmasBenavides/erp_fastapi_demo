# app/infrastructure/services/cloudinary_service.py
import os
import tempfile
import uuid
from typing import Dict, Optional, Union, List
from fastapi import UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
import aiofiles
import asyncio
from pathlib import Path
from app.core.config import configs


class CloudinaryService:
    def __init__(self):
        # Configurar Cloudinary desde las variables de entorno
        cloudinary.config(
            cloud_name=configs.CLOUDINARY_CLOUD_NAME,
            api_key=configs.CLOUDINARY_API_KEY,
            api_secret=configs.CLOUDINARY_API_SECRET,
            secure=True,
        )
        self.protected_ids = []  # Añade esta línea

    async def upload_image(
        self,
        file: UploadFile,
        folder: Optional[str] = None,
        public_id: Optional[str] = None,
        overwrite: bool = False,
    ) -> Dict:
        """
        Sube una imagen a Cloudinary
        """
        print("subiendo imagen a cloudinary")
        if not file or file.size == 0:
            raise ValueError("Archivo vacío")

        # Crear archivo temporal
        temp_file = await self._save_temp_file(file)

        try:
            upload_params = {
                "folder": folder or configs.CLOUDINARY_DEFAULT_FOLDER,
                "use_filename": True,
                "unique_filename": True,
                "overwrite": overwrite,
            }

            if public_id:
                upload_params["public_id"] = public_id
            
            print(f"Subiendo archivo temporal: {temp_file}")
            
            # ✅ CORRECCIÓN: Usar asyncio.to_thread para ejecutar función síncrona
            result = await asyncio.to_thread(
                cloudinary.uploader.upload,
                temp_file,
                **upload_params
            )
            
            print("se terminó el proceso")
            print(result)
            return self._map_upload_result(result)

        except Exception as e:
            print(f"Error en upload_image: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error al subir imagen a Cloudinary: {str(e)}"
            )
        finally:
            # Eliminar archivo temporal
            await self._delete_temp_file(temp_file)

    async def upload_file(
        self,
        file: UploadFile,
        folder: Optional[str] = None,
        resource_type: str = "auto",
    ) -> Dict:
        """
        Sube cualquier tipo de archivo a Cloudinary
        """
        if not file or file.size == 0:
            raise ValueError("Archivo vacío")

        temp_file = await self._save_temp_file(file)

        try:
            upload_params = {
                "folder": folder or configs.CLOUDINARY_DEFAULT_FOLDER,
                "use_filename": True,
                "unique_filename": True,
                "overwrite": False,
                "resource_type": resource_type,
            }

            # ✅ CORRECCIÓN: Usar asyncio.to_thread
            result = await asyncio.to_thread(
                cloudinary.uploader.upload,
                temp_file,
                **upload_params
            )

            return self._map_upload_result(result)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error al subir archivo a Cloudinary: {str(e)}"
            )
        finally:
            await self._delete_temp_file(temp_file)

    async def resource_exists(self, public_id: str) -> bool:
        """
        Verifica si un recurso existe en Cloudinary
        """
        if not public_id:
            return False

        try:
            # ✅ CORRECCIÓN: Usar asyncio.to_thread
            result = await asyncio.to_thread(
                cloudinary.api.resource,
                public_id
            )
            return result.get("public_id") == public_id
        except cloudinary.api.NotFound:
            return False
        except Exception:
            return True

    async def delete_resource(self, public_id: str) -> bool:
        """
        Elimina un recurso de Cloudinary
        """
        if not public_id:
            return False

        # Verificar si es un ID protegido
        if hasattr(self, 'protected_ids') and public_id in self.protected_ids:
            return False

        try:
            # ✅ CORRECCIÓN: Usar asyncio.to_thread
            result = await asyncio.to_thread(
                cloudinary.uploader.destroy,
                public_id,
                invalidate=True
            )
            return result.get("result") == "ok"
        except Exception as e:
            print(f"[Cloudinary] No se pudo borrar {public_id}: {e}")
            return False

    def get_email_logo_url(self, width: int = 120) -> str:
        """
        Obtiene la URL del logo para emails
        """
        logo_public_id = configs.CLOUDINARY_LOGO_PUBLIC_ID
        if not logo_public_id:
            return ""

        # Generar URL con transformaciones
        url, _ = cloudinary_url(
            logo_public_id,
            width=width,
            quality="auto",
            fetch_format="auto",
            secure=True,
        )

        return url

    def get_image_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill",
        quality: str = "auto",
        format: str = "auto",
    ) -> str:
        """
        Genera URL para una imagen con transformaciones
        """
        transformation = []

        if width and height:
            transformation.append(f"c_{crop},w_{width},h_{height}")
        elif width:
            transformation.append(f"w_{width}")
        elif height:
            transformation.append(f"h_{height}")

        url, _ = cloudinary_url(
            public_id,
            transformation=transformation,
            quality=quality,
            fetch_format=format,
            secure=True,
        )

        return url

    async def upload_multiple_images(
        self, files: List[UploadFile], folder: Optional[str] = None
    ) -> List[Dict]:
        """
        Sube múltiples imágenes simultáneamente
        """
        tasks = [self.upload_image(file, folder) for file in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtrar resultados exitosos
        upload_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error subiendo archivo: {result}")
                continue
            upload_results.append(result)

        return upload_results

    # -------------------- Métodos auxiliares --------------------

    async def _save_temp_file(self, file: UploadFile) -> str:
        """
        Guarda el archivo temporalmente
        """
        # Crear nombre único
        ext = Path(file.filename).suffix if file.filename else ".tmp"
        temp_filename = f"upload_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(tempfile.gettempdir(), temp_filename)

        # Guardar contenido
        async with aiofiles.open(temp_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        # Resetear cursor del archivo
        await file.seek(0)

        return temp_path

    async def _delete_temp_file(self, file_path: str):
        """
        Elimina archivo temporal
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass  # Ignorar errores al eliminar temporal

    def _map_upload_result(self, result: Dict) -> Dict:
        """
        Mapea el resultado de Cloudinary a un formato estándar
        """
        return {
            "public_id": result.get("public_id"),
            "url": result.get("url"),
            "secure_url": result.get("secure_url"),
            "resource_type": result.get("resource_type"),
            "format": result.get("format"),
            "bytes": result.get("bytes"),
            "width": result.get("width"),
            "height": result.get("height"),
            "created_at": result.get("created_at"),
        }
