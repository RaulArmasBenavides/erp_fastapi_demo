from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.user import User

 

class IUserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(
        self,
        user_id: int,
        *,
        name: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[User]:
        pass

    @abstractmethod
    def soft_delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def list_users(
        self,
        *,
        only_active: bool = True,
        role: Optional[str] = None,
    ) -> List[User]:
        """
        Lista usuarios del sistema.

        :param only_active: si True, solo usuarios activos
        :param role: Requester | Approver | None
        """
        pass
