from pydantic import BaseModel, EmailStr, Field

from typing import Optional
from datetime import datetime


# @dataclass(frozen=True)
class User(BaseModel):
    id: Optional[int]
    email: str
    name: Optional[str]
    is_active: bool
    role: str = "Requester"
    password: str = None
    # para auth interna (no exponer)
    password_hash: Optional[str] = Field(default=None, exclude=True)
    created_at: Optional[datetime] = None
