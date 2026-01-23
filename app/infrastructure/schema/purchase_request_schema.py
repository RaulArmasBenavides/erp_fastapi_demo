# app/infrastructure/schema/purchase_request_schema.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.infrastructure.repository.database import ORMBase
 
class PurchaseRequestSchema(ORMBase):
    __tablename__ = "purchase_requests"

    id = Column(Integer, primary_key=True, index=True)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, index=True)
    requested_by_user_id = Column(Integer, nullable=False, index=True)

    description = Column(String(500), nullable=False)
    status = Column(String(30), nullable=False, default="draft")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
