# app/core/models/supplier.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SupplierModel(BaseModel):
    id: Optional[int] = None
    name: str
    address: str
    phone: str
    email: EmailStr
    photo: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    is_approved: bool = False
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None