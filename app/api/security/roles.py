from typing import Callable
from fastapi import Depends, HTTPException, status

from app.api.security.current_user import get_current_user
from app.infrastructure.schema.user_schema import UserSchema
 

def require_any_role(*roles: str) -> Callable:
    allowed = {r.strip() for r in roles if r and r.strip()}

    def _checker(user: UserSchema = Depends(get_current_user)) -> UserSchema:
        if not user or not getattr(user, "is_active", True):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        role = (getattr(user, "role", None) or "").strip()
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: requires one of roles {sorted(allowed)}"
            )

        return user

    return _checker
