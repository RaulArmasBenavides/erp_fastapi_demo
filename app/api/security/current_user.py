from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.container import Container
from app.infrastructure.repository.user_repository import UserRepository
from app.infrastructure.schema.user_schema import UserSchema
from app.core.config import configs
from jose import jwt, JWTError
from dependency_injector.wiring import Provide, inject

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")
@inject
def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_repo: UserRepository = Depends(Provide[Container.user_repository]),
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise credentials_exception

    email: Optional[str] = payload.get("email")
    sub: Optional[str] = payload.get("sub")

    if not email and not sub:
        raise credentials_exception

    # Cargar usuario desde DB (recomendado por email)
    user = users_repo.get_by_email(email) if email else None

    # Si tu repo soporta búsqueda por id, puedes fallback:
    # if user is None and sub is not None and sub.isdigit():
    #     user = users_repo.get_by_id(int(sub))

    if user is None:
        raise credentials_exception

    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user
