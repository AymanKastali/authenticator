from datetime import datetime, timezone
from uuid import UUID

from fastapi import Depends, HTTPException, status

from application.dto.auth.jwt.payload import JwtPayloadDto
from application.services.auth.jwt.auth import JwtAuthService
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.value_objects.identifiers import UUIDVo
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)
from presentation.web.fastapi.api.v1.dependencies.application.jwt import (
    jwt_auth_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.jwt import (
    jwt_authenticated_user_controller_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.jwt import (
    jwt_redis_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.security.oauth2 import (
    oauth2_scheme,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


async def validate_jwt_token(
    token: str,
    jwt_auth_service: JwtAuthService,
    redis: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> JwtPayloadDto:
    try:
        payload = jwt_auth_service.verify_jwt_token(token)
        now = datetime.now(timezone.utc).timestamp()
        if now >= payload.exp:
            raise JwtExpiredError("Token expired")
        if await redis.is_jwt_blacklisted(UUIDVo.from_string(payload.jti)):
            raise JwtInvalidError("Token revoked/blacklisted")
        return payload
    except (JwtExpiredError, JwtInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


async def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    jwt_auth_service: JwtAuthService = Depends(jwt_auth_service_dependency),
    user_controller=Depends(jwt_authenticated_user_controller_dependency),
    redis: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> AuthenticatedUserResponseSchema:
    payload = await validate_jwt_token(token, jwt_auth_service, redis)
    return await user_controller.execute(UUID(payload.sub))


def get_current_authenticated_active_user(
    current_user: AuthenticatedUserResponseSchema = Depends(
        get_current_authenticated_user
    ),
) -> AuthenticatedUserResponseSchema:
    if current_user.status.lower() != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
