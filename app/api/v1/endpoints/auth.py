# app/api/v1/endpoints/auth.py
from app.core.models.user import User
from app.infrastructure.schema.auth_schema import SignIn, SignInResponse, SignUp
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.container import Container
from app.core.exceptions import AuthError
from app.core.interfaces.i_auth_service import IAuthService
from app.infrastructure.schema.user_schema import UserSchema
 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(
    user_info: SignIn,
    service: IAuthService = Depends(Provide[Container.auth_service]),
):
    try:
        return service.sign_in(user_info)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/sign-up", response_model=User)
@inject
async def sign_up(
    user_info: SignUp,
    service: IAuthService = Depends(Provide[Container.auth_service]),
):
    try:
        return service.sign_up(user_info)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
