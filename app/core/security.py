# --------- Helpers internos ---------
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from app.core.config import configs

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = configs.SECRET_KEY
exp_minutes = int(configs.ACCESS_TOKEN_EXPIRE_MINUTES or 60)


def hash_password(self, plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(self, plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(self, *, sub: str, email: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=exp_minutes)
    payload = {
        "sub": sub,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)
