from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dto.user_response import UserResponse
from app.application.services.user_admin_service import UserAdminService
from app.core.models.user import User
from dependency_injector.wiring import Provide, inject

from app.api.security.roles import require_any_role
from app.core.container import Container
 
 
from app.infrastructure.schema.user_schema import UserSchema  # (tu current_user devuelve esto o tu User Pydantic)
 

router = APIRouter(prefix="/users", tags=["users-admin"])


@router.get("/", response_model=List[UserResponse])
@inject
def list_users(
    user: UserSchema = Depends(require_any_role("Requester", "Approver")),
    service: UserAdminService = Depends(Provide[Container.user_admin_service]),
):
    users = service.list_users()
    return [UserResponse.from_domain(u) for u in users]


@router.get("/{user_id}", response_model=User)
@inject
def get_user(
    user_id: int,
    user: UserSchema = Depends(require_any_role("Approver")),
    service: UserAdminService = Depends(Provide[Container.user_admin_service]),
):
    u = service.get_user(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_domain(u)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    body: User,
    user: UserSchema = Depends(require_any_role("Approver")),
    service: UserAdminService = Depends(Provide[Container.user_admin_service]),
):
    created = service.create_user(body)
    return User.from_domain(created)


@router.patch("/{user_id}", response_model=User)
@inject
def patch_user(
    user_id: int,
    body: User,
    user: UserSchema = Depends(require_any_role("Approver")),
    service: UserAdminService = Depends(Provide[Container.user_admin_service]),
):
    updated = service.patch_user(user_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_domain(updated)

 

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def soft_delete_user(
    user_id: int,
    user: UserSchema = Depends(require_any_role("Approver")),
    service: UserAdminService = Depends(Provide[Container.user_admin_service]),
):
    ok = service.soft_delete(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return
