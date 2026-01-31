from typing import Optional
from app.core.config import configs
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.user import User
from app.infrastructure.schema.auth_schema import SignIn, SignInResponse, SignUp


class AuthError(Exception):
    pass


class AuthService:
    """Casos de uso de autenticación: sign-up y sign-in."""

    def __init__(self, user_repository):
        # user_repository debe exponer: get_by_email(email) -> Optional[User], create(user: User) -> User
        self._users = user_repository

    # --------- API pública ---------
    def sign_up(self, payload: SignUp) -> User:
        if self._users.get_by_email(payload.email):
            raise AuthError("Email ya registrado")

        hashed = hash_password(payload.password)

        new_user = User(
            id=None,
            email=payload.email,
            name=getattr(payload, "full_name", None),  # mapeo simple
            is_active=True,
            role="Requester",  # default
            password_hash=hashed,
            created_at=None,
        )

        return self._users.create(new_user)

    def sign_in(self, payload: SignIn) -> SignInResponse:
        # 1) buscar usuario
        user: Optional[User] = self._users.get_by_email(payload.email)
        if not user:
            raise AuthError("Credenciales inválidas")

        # 2) validar pass
        hashed = getattr(user, "password_hash", None)
        if not hashed or not verify_password(payload.password, hashed):
            raise AuthError("Credenciales inválidas")

        # 3) emitir token
        token = create_access_token(sub=str(user.id), email=user.email)

        # 4) armar respuesta
        return SignInResponse(access_token=token, token_type="bearer", user=user)
