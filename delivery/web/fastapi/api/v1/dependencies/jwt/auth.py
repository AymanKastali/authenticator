from datetime import datetime, timezone
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from adapters.exceptions.adapters_errors import JWTExpiredError, JWTInvalidError
from application.dto.auth.jwt.token import JwtDto
from delivery.bootstrap.containers.auth import jwt_auth_container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> AuthenticatedUserOutDto:
    try:
        token_dto: JwtDto = jwt_auth_container.jwt_service.verify(token)
        payload_dto = token_dto.payload

        if datetime.now(timezone.utc).timestamp() >= payload_dto.exp:
            raise JWTExpiredError("Token expired")

        if jwt_auth_container.jwt_repo.is_token_blacklisted(payload_dto.jti):
            raise JWTInvalidError("Token revoked/blacklisted")

    except (JWTExpiredError, JWTInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    user = jwt_auth_container.authenticated_user_controller.execute(
        UUID(payload_dto.sub)
    )
    return user


def get_current_active_user(
    current_user: AuthenticatedUserOutDto = Depends(get_current_user),
):
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
