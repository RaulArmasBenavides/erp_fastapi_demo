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
                name=row.name,
                is_active=row.is_active,
                role=row.role,
                password_hash=row.password_hash,   # <- este es el hash real
                created_at=row.created_at,
            )

    def create(self, user: User) -> User:
        with self._db.session() as session:
            row = UserSchema(
                email=str(user.email).strip().lower(),
                name=user.name,
                is_active=user.is_active,
                role=getattr(user, "role", None) or "Requester",
                password_hash=user.password_hash,  # ✅ campo real
                # user_token: si lo usas, setéalo aquí
                # user_token=getattr(user, "user_token", None),
            )

            session.add(row)
            session.commit()
            session.refresh(row)

            return User(
                id=row.id,
                email=row.email,
                name=row.name,
                is_active=row.is_active,
                role=row.role,
                password_hash=row.password_hash,
                created_at=row.created_at,
            )