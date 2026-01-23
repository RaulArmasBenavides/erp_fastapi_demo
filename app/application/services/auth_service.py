from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext
from app.core.models.config import configs

from app.infrastructure.schema.user_schema import User


class AuthError(Exception):
    pass


class AuthService:
    """Casos de uso de autenticación: sign-up y sign-in."""
    def __init__(self, user_repository):
        # user_repository debe exponer: get_by_email(email) -> Optional[User], create(user: User) -> User
        self._users = user_repository
        self._pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._secret = configs.SECRET_KEY
        self._exp_minutes = int(configs.ACCESS_TOKEN_EXPIRE_MINUTES or 60)

    # --------- API pública ---------
    def sign_up(self, payload: SignUp) -> User:
        # 1) existe?
        if self._users.get_by_email(payload.email):
            raise AuthError("Email ya registrado")

        # 2) hash pass
        hashed = self._hash_password(payload.password)

        # 3) construir User DTO (ajusta campos según tu User)
        new_user = User(
            id=0,                      # el repo debe asignar ID
            email=payload.email,
            full_name=getattr(payload, "full_name", None),
            is_active=True,
            hashed_password=hashed,    # si tu User no lo expone, quítalo y mapea en el repo
        )

        # 4) persistir
        created = self._users.create(new_user)
        # Opcional: no retornar hashed_password al cliente; asegura que tu User (Pydantic) lo oculte
        return created

    def sign_in(self, payload: SignIn) -> SignInResponse:
        # 1) buscar usuario
        user: Optional[User] = self._users.get_by_email(payload.email)
        if not user:
            raise AuthError("Credenciales inválidas")

        # 2) validar pass
        hashed = getattr(user, "hashed_password", None)
        if not hashed or not self._verify_password(payload.password, hashed):
            raise AuthError("Credenciales inválidas")

        # 3) emitir token
        token = self._create_access_token(sub=str(user.id), email=user.email)

        # 4) armar respuesta
        return SignInResponse(
            access_token=token,
            token_type="bearer",
            user=user
        )

    # --------- Helpers internos ---------
    def _hash_password(self, plain: str) -> str:
        return self._pwd.hash(plain)

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return self._pwd.verify(plain, hashed)

    def _create_access_token(self, *, sub: str, email: str) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=self._exp_minutes)
        payload = {
            "sub": sub,
            "email": email,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")
