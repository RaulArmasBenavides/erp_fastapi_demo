# app/infrastructure/repositories/supplier_repository.py
from datetime import datetime
from typing import List, Optional

from app.core.interfaces.i_supplier_repository import ISupplierRepository
 
from app.domain.supplier import SupplierModel
from app.infrastructure.repository.database import Database
from app.infrastructure.schema.supplier_schema import SupplierSchema


class SupplierRepository(ISupplierRepository):
    def __init__(self, db: Database):
        self._db = db

    def add_supplier(self, supplier: SupplierModel, created_by: str) -> SupplierModel:
        created_by = (created_by or "").strip()
        if not created_by:
            raise ValueError("created_by es requerido")
        with self._db.session() as session:
            row = SupplierSchema(
                name=supplier.name,
                address=supplier.address,
                phone=supplier.phone,
                email=str(supplier.email),
                photo=supplier.photo,
                created_at=datetime.utcnow(),
                created_by=created_by,
                is_approved=getattr(supplier, "is_approved", False),
                approved_at=getattr(supplier, "approved_at", None),
                approved_by=getattr(supplier, "approved_by", None),
            )
            session.add(row)
            session.commit()
            session.refresh(row)

            return SupplierModel(
                id=row.id,
                name=row.name,
                address=row.address,
                phone=row.phone,
                email=row.email,
                photo=row.photo,
                is_approved=row.is_approved,
                approved_at=row.approved_at,
                approved_by=row.approved_by,
            )

    def view_suppliers(self) -> List[SupplierModel]:
        with self._db.session() as session:
            rows = (
                session.query(SupplierSchema).order_by(SupplierSchema.id.desc()).all()
            )

            return [
                SupplierModel(
                    id=r.id,
                    name=r.name,
                    address=r.address,
                    phone=r.phone,
                    email=r.email,
                    photo=r.photo,
                    is_approved=r.is_approved,
                    created_by=r.created_by,
                    created_at=r.created_at,
                    approved_at=r.approved_at,
                    approved_by=r.approved_by,
                )
                for r in rows
            ]

    def delete_supplier(self, supplier_id: int) -> None:
        with self._db.session() as session:
            row = session.get(SupplierSchema, supplier_id)
            if row is None:
                return  # o lanza excepción si prefieres

            session.delete(row)
            session.commit()

    def approve_supplier(
        self, supplier_id: int, approved_by: str
    ) -> Optional[SupplierModel]:
        """
        Marca el supplier como aprobado.
        - Si no existe: None
        - Si ya está aprobado: retorna el estado actual (idempotente)
        """
        approved_by = (approved_by or "").strip()
        if not approved_by:
            raise ValueError("approved_by es requerido")

        with self._db.session() as session:
            row = session.get(SupplierSchema, supplier_id)
            if row is None:
                return None

            # Idempotente: si ya está aprobado, solo devuelve
            if not getattr(row, "is_approved", False):
                row.is_approved = True
                row.approved_at = datetime.utcnow()
                row.approved_by = approved_by
                session.add(row)
                session.commit()
                session.refresh(row)

            return SupplierModel(
                id=row.id,
                name=row.name,
                address=row.address,
                phone=row.phone,
                email=row.email,
                photo=row.photo,
                is_approved=row.is_approved,
                approved_at=row.approved_at,
                approved_by=row.approved_by,
            )

    def get_supplier(self, supplier_id: int) -> Optional[SupplierModel]:
        with self._db.session() as session:
            row = session.get(SupplierSchema, supplier_id)
            if row is None:
                return None

            return SupplierModel(
                id=row.id,
                name=row.name,
                address=row.address,
                phone=row.phone,
                email=row.email,
                photo=row.photo,
                is_approved=row.is_approved,
                created_by=row.created_by,
                created_at=row.created_at,
                approved_at=row.approved_at,
                approved_by=row.approved_by,
            )

    def update_supplier(
        self, supplier_id: int, update_data: dict
    ) -> Optional[SupplierModel]:
        with self._db.session() as session:
            row = session.get(SupplierSchema, supplier_id)
            if row is None:
                return None

            # Actualizar los campos proporcionados
            for key, value in update_data.items():
                if hasattr(row, key):
                    setattr(row, key, value)

 
            session.add(row)
            session.commit()
            session.refresh(row)

            return SupplierModel(
                id=row.id,
                name=row.name,
                address=row.address,
                phone=row.phone,
                email=row.email,
                photo=row.photo,
                is_approved=row.is_approved,
                created_by=row.created_by,
                created_at=row.created_at,
                approved_at=row.approved_at,
                approved_by=row.approved_by,
            )
