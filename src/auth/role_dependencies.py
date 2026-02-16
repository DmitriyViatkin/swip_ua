from fastapi import Depends, HTTPException, status
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.enums import UserRole


def require_roles(*allowed_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != UserRole.SUPERADMIN and current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )

        # ---------------------
        return current_user

    # ---------------------
    return role_checker