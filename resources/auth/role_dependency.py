from fastapi import Depends, HTTPException, status
from resources.schemas.response import UserRole, User, ROLE_HIERARCHY
from resources.auth.auth_service import get_current_user


def require_minimum_role(required_role: UserRole):
    """
    Check if the current user's role is at least the required role.
    """

    async def role_dependency(current_user: User = Depends(get_current_user)):
        current_role_level = ROLE_HIERARCHY.get(current_user.role, 0)
        required_role_level = ROLE_HIERARCHY.get(required_role, 0)
        if current_role_level < required_role_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return role_dependency
