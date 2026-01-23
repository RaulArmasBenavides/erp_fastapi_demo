from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PurchaseRequestModel(BaseModel):
    id: Optional[int] = None
    supplier_id: int
    requested_by_user_id: int  # el usuario que la creó
    description: str
    status: str = "draft"      # draft/approved/rejected/ordered
    created_at: Optional[datetime] = None