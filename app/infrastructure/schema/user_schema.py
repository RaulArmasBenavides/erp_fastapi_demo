from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class UserEntity(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(index=True, unique=True, nullable=False)

    # persistencia: guarda hash, no password plano
    password_hash: str = Field(nullable=False)

    # opcional si realmente lo usas
    user_token: Optional[str] = Field(default=None, unique=True, index=True)

    name: Optional[str] = Field(default=None, nullable=True)

    is_active: bool = Field(default=True, nullable=False)

    # reemplaza is_superuser
    role: str = Field(default="user", index=True, nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)