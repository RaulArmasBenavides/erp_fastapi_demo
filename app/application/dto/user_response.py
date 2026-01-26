from app.application.services.user_admin_service import UserAdminService
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.core.models.user import User


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    is_active: bool
    role: str
    created_at: Optional[datetime]

    @staticmethod
    def from_domain(user: User) -> "UserResponse":
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at,
        )