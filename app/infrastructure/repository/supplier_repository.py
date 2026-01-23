# app/infrastructure/repositories/supplier_repository.py
from typing import List

from app.core.interfaces.IEntryRepository import IEntryRepository  # NO: solo referencia; quítalo
from app.core.models.supplier import SupplierModel
from app.infrastructure.repository.database import Database
from app.infrastructure.schema.supplier_schema import SupplierSchema
 

class SupplierRepository:
    def __init__(self, db: Database):
        self._db = db

    def add_supplier(self, supplier: SupplierModel) -> SupplierModel:
        with self._db.session() as session:
            row = SupplierSchema(
                name=supplier.name,
                address=supplier.address,
                phone=supplier.phone,
                email=str(supplier.email),
                photo=supplier.photo,
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
            )

    def view_suppliers(self) -> List[SupplierModel]:
        with self._db.session() as session:
            rows = session.query(SupplierSchema).order_by(SupplierSchema.id.desc()).all()

            return [
                SupplierModel(
                    id=r.id,
                    name=r.name,
                    address=r.address,
                    phone=r.phone,
                    email=r.email,
                    photo=r.photo,
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
