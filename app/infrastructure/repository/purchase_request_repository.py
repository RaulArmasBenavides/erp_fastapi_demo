# app/infrastructure/repositories/purchase_request_repository.py
from typing import List
 
from app.core.interfaces.i_purchase_request_repository import IPurchaseRequestRepository
from app.domain.purchase_request import PurchaseRequestModel
from app.infrastructure.repository.database import Database
from app.infrastructure.schema.purchase_request_schema import PurchaseRequestSchema
 
class PurchaseRequestRepository(IPurchaseRequestRepository):
    def __init__(self, db: Database):
        self._db = db

    def add_request(self, pr: PurchaseRequestModel) -> PurchaseRequestModel:
        with self._db.session() as session:
            row = PurchaseRequestSchema(
                supplier_id=pr.supplier_id,
                requested_by_user_id=pr.requested_by_user_id,
                description=pr.description,
                status=pr.status,
            )
            session.add(row)
            session.commit()
            session.refresh(row)

            return PurchaseRequestModel(
                id=row.id,
                supplier_id=row.supplier_id,
                requested_by_user_id=row.requested_by_user_id,
                description=row.description,
                status=row.status,
                created_at=row.created_at,
            )

    def list_by_supplier(self, supplier_id: int) -> List[PurchaseRequestModel]:
        with self._db.session() as session:
            rows = (
                session.query(PurchaseRequestSchema)
                .filter(PurchaseRequestSchema.supplier_id == supplier_id)
                .order_by(PurchaseRequestSchema.id.desc())
                .all()
            )
            return [
                PurchaseRequestModel(
                    id=r.id,
                    supplier_id=r.supplier_id,
                    requested_by_user_id=r.requested_by_user_id,
                    description=r.description,
                    status=r.status,
                    created_at=r.created_at,
                )
                for r in rows
            ]
