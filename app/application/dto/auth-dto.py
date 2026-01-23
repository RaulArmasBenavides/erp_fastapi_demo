from datetime import datetime
from pydantic import BaseModel, EmailStr


class SignIn(BaseModel):
    email: EmailStr
    password: str


class SignUp(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expiration: datetime
    user: UserPublic
