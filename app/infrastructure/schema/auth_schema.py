from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class SignUp(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=120)


class SignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: object  # luego lo tipamos bien
