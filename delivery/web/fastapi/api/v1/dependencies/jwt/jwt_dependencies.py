from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from adapters.presenters.response_models.user_response_models import (
    AuthenticatedUserResponseModel,
)
from delivery.bootstrap.di_container import container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/jwt")


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> AuthenticatedUserResponseModel:
    payload = container.jwt_service.verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = container.get_user_controller.execute(UUID(payload.sub))
    return user


def get_current_active_user(
    current_user: AuthenticatedUserResponseModel = Depends(get_current_user),
):
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user


def auth_required():
    """Helper for route-level dependency injection."""
    return Depends(get_current_active_user)
