from typing import List, Optional

from app.core.interfaces.i_user_repository import IUserRepository
 
from app.domain.user import User
from app.infrastructure.repository.database import Database

from app.infrastructure.schema.user_schema import (
    UserSchema,
)  # <-- este debe ser tu SQLAlchemy model


class UserRepository(IUserRepository):
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
                password_hash=row.password_hash,  # <- este es el hash real
                created_at=row.created_at,
            )

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self._db.session() as session:
            row = session.get(UserSchema, user_id)

            if row is None:
                return None

            return User(
                id=row.id,
                email=row.email,
                name=row.name,
                is_active=row.is_active,
                role=row.role,
                password_hash=row.password_hash,
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

    def update(
        self,
        user_id: int,
        *,
        name: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[User]:

        with self._db.session() as session:
            row = session.get(UserSchema, user_id)

            if row is None:
                return None

            if name is not None:
                row.name = name

            if role is not None:
                row.role = role  # Requester | Approver

            if is_active is not None:
                row.is_active = is_active

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

    def soft_delete(self, user_id: int) -> bool:
        with self._db.session() as session:
            row = session.get(UserSchema, user_id)

            if row is None:
                return False

            row.is_active = False

            session.add(row)
            session.commit()
            return True

    def list_users(
        self,
        *,
        only_active: bool = True,
        role: Optional[str] = None,
    ) -> List[User]:
        with self._db.session() as session:
            query = session.query(UserSchema)

            if only_active:
                query = query.filter(UserSchema.is_active.is_(True))

            if role:
                query = query.filter(UserSchema.role == role)

            rows = query.order_by(UserSchema.created_at.desc()).all()

            return [self._to_domain(row) for row in rows]

    def _to_domain(self, row: Optional[UserSchema]) -> Optional[User]:
        if row is None:
            return None

        return User(
            id=row.id,
            email=row.email,
            name=row.name,
            is_active=row.is_active,
            role=row.role,
            password_hash=row.password_hash,
            created_at=row.created_at,
        )
