from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.infrastructure.repository.database import ORMBase


class UserSchema(ORMBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(200), nullable=False, unique=True, index=True)

    password_hash = Column(String(300), nullable=False)

    user_token = Column(String(300), nullable=True, unique=True, index=True)

    name = Column(String(200), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    role = Column(String(50), nullable=False, default="Requester", index=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
