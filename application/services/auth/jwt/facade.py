# application/facades/jwt_auth_facade.py
from datetime import datetime, timezone

from application.dto.auth.jwt.token import JwtDto
from application.mappers.jwt import JwtMapper

# from application.ports.cache.redis.jwt_blacklist import (
#     AsyncJwtBlacklistRedisPort,
# )
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity


class JwtAuthFacade:
    """Coordinates authentication, JWT creation, validation, and blacklist."""

    def __init__(
        self,
        auth_service: AuthService,
        jwt_auth_service: JwtAuthService,
        # blacklist_cache: AsyncJwtBlacklistRedisPort,
    ):
        self._auth_service = auth_service
        self._jwt_auth_service = jwt_auth_service
        # self._blacklist_cache = blacklist_cache

    # ------------------- Login / Token -------------------

    def _generate_jwt_tokens(self, user: UserEntity) -> dict[str, str]:
        access_token: JwtEntity = self._jwt_auth_service.create_access_token(
            user
        )
        refresh_token: JwtEntity = self._jwt_auth_service.create_refresh_token(
            user
        )
        return {
            "access_token": access_token.signature,
            "refresh_token": refresh_token.signature,
        }

    def login_user(self, email: str, password: str) -> dict[str, str]:
        user: UserEntity = self._auth_service.authenticate_user(email, password)
        return self._generate_jwt_tokens(user)

    def refresh_jwt_token(self, refresh_token: str) -> dict[str, str]:
        token: JwtEntity = self._jwt_auth_service.verify_refresh_token(
            refresh_token
        )
        user_id = token.payload.sub
        user: UserEntity = self._auth_service.get_user_by_id(user_id.to_uuid())
        return self._generate_jwt_tokens(user)

    # ------------------- Logout / Blacklist -------------------
    async def logout(self, token: str) -> None:
        # Verify and decode token
        token_entity: JwtEntity = self._jwt_auth_service.verify_token(token)
        jti: str = token_entity.payload.jti.to_string()

        # Calculate absolute expiration timestamp
        exp_timestamp: float = token_entity.payload.exp.timestamp()
        now_timestamp: float = datetime.now(timezone.utc).timestamp()

        # Only blacklist if token has time remaining
        # if exp_timestamp > now_timestamp:
        #     # Pass absolute expiration timestamp to adapter
        #     await self._blacklist_cache.blacklist_jwt(
        #         jti=jti, expire_at=int(exp_timestamp)
        #     )

    # ------------------- Validation -------------------
    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtDto:
        token_entity: JwtEntity = self._jwt_auth_service.verify_token(
            token, subject
        )
        token_dto: JwtDto = JwtMapper.to_jwt_dto_from_entity(token_entity)
        return token_dto
