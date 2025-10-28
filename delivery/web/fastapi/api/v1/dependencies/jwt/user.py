from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)
from adapters.exceptions.adapters_errors import JWTExpiredError, JWTInvalidError
from application.dto.jwt_dto import JwtTokenPayloadDto
from delivery.bootstrap.containers.auth import jwt_auth_container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> AuthenticatedUserResponseModel:
    try:
        payload: JwtTokenPayloadDto = jwt_auth_container.jwt_service.verify(
            token
        )
    except (JWTExpiredError, JWTInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e
        ) from e

    user = jwt_auth_container.get_user_controller.execute(UUID(payload.sub))
    return user


def get_current_active_user(
    current_user: AuthenticatedUserResponseModel = Depends(get_current_user),
):
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
