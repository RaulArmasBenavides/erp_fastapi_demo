from typing import Protocol
from app.infrastructure.schema.auth_schema import SignIn, SignInResponse, SignUp
from app.infrastructure.schema.user_schema import UserSchema

class IAuthService(Protocol):
    def sign_up(self, payload: SignUp) -> UserSchema: ...
    def sign_in(self, payload: SignIn) -> SignInResponse: ...
