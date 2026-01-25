from typing import Optional

from app.core.models.user import User
from app.infrastructure.repository.database import Database
 
from app.infrastructure.schema.user_schema import (
    UserSchema,
)  # <-- este debe ser tu SQLAlchemy model


class UserRepository:
    def __init__(self, db: Database):
        self._db = db

    def get_by_email(self, email: str) -> Optional[User]:
        email = (email or "").strip().lower()
        if not email:
            return None

        with self._db.session() as session:
            row = session.query(UserSchema).filter(UserSchema.email == email).first()

            if row is None:
                return None

            # Importante: esto devuelve el User (Pydantic) para que AuthService lea hashed_password
            return User(
                id=row.id,
                email=row.email,
                full_name=getattr(row, "full_name", None),
                is_active=getattr(row, "is_active", True),
                hashed_password=getattr(row, "hashed_password", None),
            )

    def create(self, user: User) -> User:
        with self._db.session() as session:
            row = UserSchema(
                email=str(user.email).strip().lower(),
                full_name=getattr(user, "full_name", None),
                is_active=getattr(user, "is_active", True),
                hashed_password=getattr(user, "hashed_password", None),
            )

            session.add(row)
            session.commit()
            session.refresh(row)

            return User(
                id=row.id,
                email=row.email,
                full_name=getattr(row, "full_name", None),
                is_active=getattr(row, "is_active", True),
                hashed_password=getattr(row, "hashed_password", None),
            )
