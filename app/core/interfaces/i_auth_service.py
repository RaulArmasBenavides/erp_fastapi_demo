from typing import Protocol
from app.core.models.user import User
from app.infrastructure.schema.auth_schema import SignIn, SignInResponse, SignUp
 
class IAuthService(Protocol):
    def sign_up(self, payload: SignUp) -> User: ...
    def sign_in(self, payload: SignIn) -> SignInResponse: ...
