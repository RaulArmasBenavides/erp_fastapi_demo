from passlib.context import CryptContext

from app.core.interfaces.i_user_repository import IUserRepository
from app.core.models.user import User


class UserAdminService:
    def __init__(self, repo: IUserRepository):
        self._repo = repo
        self._pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def list_users(self):
        return self._repo.list_users()

    def get_user(self, user_id: int):
        return self._repo.get_by_id(user_id)

    def create_user(self, dto: User) -> User:
        password_hash = self._pwd.hash(dto.password)

        user = User(
            id=None,
            email=dto.email,
            name=dto.name,
            is_active=dto.is_active,
            role=dto.role,
            password_hash=password_hash,
            created_at=None,
        )
        return self._repo.create(user)

    def patch_user(self, user_id: int, dto: User):
        return self._repo.patch(
            user_id, name=dto.name, is_active=dto.is_active, role=dto.role
        )

    def reset_password(self, user_id: int, new_password: str):
        password_hash = self._pwd.hash(new_password)
        return self._repo.set_password_hash(user_id, password_hash)

    def soft_delete(self, user_id: int) -> bool:
        return self._repo.soft_delete(user_id)
