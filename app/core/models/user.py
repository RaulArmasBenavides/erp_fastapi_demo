from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class UserModel:
    id: Optional[int]
    email: str
    name: Optional[str]
    is_active: bool
    role: str
    created_at: Optional[datetime] = None