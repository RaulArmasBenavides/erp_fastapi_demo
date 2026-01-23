import datetime
from app.core.models.user import UserPublic
from pydantic import BaseModel


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: UserPublic