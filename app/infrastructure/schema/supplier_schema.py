# app/infrastructure/schema/supplier_schema.py
from app.infrastructure.repository.database import ORMBase
from sqlalchemy import Boolean, Column, DateTime, Integer, String
 
class SupplierSchema(ORMBase):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(400), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    photo = Column(String(300), nullable=True)  # GUID / public_id Cloudinary
    is_approved = Column(Boolean, nullable=False, default=False)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(String(200), nullable=True)