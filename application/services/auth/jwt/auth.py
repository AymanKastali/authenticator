from uuid import UUID

from application.dto.auth.jwt.token import JwtDto
from application.dto.auth.jwt.tokens_config import TokensConfigDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.jwt import JwtMapper
from application.mappers.user import UserMapper
from application.ports.cache.redis.jwt_blacklist import (
    AsyncJwtBlacklistRedisPort,
)
from application.ports.services.jwt import JwtServicePort
from application.services.auth.authentication import AuthService
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.utils.time import expires_after, utc_now_time_stamp
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    """Responsible for signing and verifying JWTs."""

    def __init__(
        self,
        auth_service: AuthService,
        jwt_service: JwtServicePort,
        tokens_config: TokensConfigDto,
        blacklist_cache: AsyncJwtBlacklistRedisPort,
    ):
        self._auth_service = auth_service
        self._jwt_service = jwt_service
        self._tokens_config = tokens_config
        self._blacklist_cache = blacklist_cache

    def _create_token(
        self, user: UserEntity, token_type: JwtTokenType, exp_seconds: int
    ) -> JwtDto:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=token_type,
            roles=list(user.roles),
            exp=expires_after(seconds=exp_seconds),
            iss=self._tokens_config.issuer,
            aud=self._tokens_config.audience,
        )
        payload_dto = JwtMapper.to_payload_dto_from_vo(payload_vo)
        token_dto: JwtDto = self._jwt_service.sign(payload_dto)
        token_entity = JwtEntity.create_signed(
            payload=payload_vo, signature=token_dto.signature
        )
        return JwtMapper.to_jwt_dto_from_entity(token_entity)

    def _create_access_token(self, user: UserEntity) -> JwtDto:
        return self._create_token(
            user=user,
            token_type=JwtTokenType.ACCESS,
            exp_seconds=self._tokens_config.access_token_exp,
        )

    def _create_refresh_token(self, user: UserEntity) -> JwtDto:
        return self._create_token(
            user=user,
            token_type=JwtTokenType.REFRESH,
            exp_seconds=self._tokens_config.refresh_token_exp,
        )

    def _create_tokens(self, user: UserEntity) -> dict[str, str]:
        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)
        return {
            "access_token": access_token.signature,
            "refresh_token": refresh_token.signature,
        }

    async def login(self, email: str, password: str) -> dict[str, str]:
        user_persistence_dto: PersistenceUserDto = (
            await self._auth_service.authenticate_user(email, password)
        )
        user_entity: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )
        return self._create_tokens(user_entity)

    async def logout(self, token: str) -> None:
        # Verify and decode token
        token_dto: JwtDto = self._jwt_service.verify(token)

        # Calculate absolute expiration timestamp
        exp_timestamp: float = token_dto.payload.exp
        now_timestamp: float = utc_now_time_stamp()

        # Only blacklist if token has time remaining
        if exp_timestamp > now_timestamp:
            # Pass absolute expiration timestamp to adapter
            await self._blacklist_cache.blacklist_jwt(
                jti=token_dto.payload.jti, expire_at=int(exp_timestamp)
            )

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtDto:
        """Verify a token and return the full DTO."""
        jwt_dto: JwtDto = self._jwt_service.verify(token, subject)
        _ = JwtMapper.to_entity_from_jwt_dto(jwt_dto).payload
        return jwt_dto

    def verify_refresh_token(self, token: str) -> JwtDto:
        """Verify a refresh token and return the full DTO."""
        jwt_dto: JwtDto = self._jwt_service.verify_refresh_token(token)
        _ = JwtMapper.to_entity_from_jwt_dto(jwt_dto).payload
        return jwt_dto

    async def refresh_jwt_token(self, refresh_token: str) -> dict[str, str]:
        token_dto: JwtDto = self.verify_refresh_token(refresh_token)
        user_id = token_dto.payload.sub
        user_persistence_dto: PersistenceUserDto = (
            await self._auth_service.get_user_by_id(UUID(user_id))
        )
        user_entity: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )
        return self._create_tokens(user_entity)

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        return await self._blacklist_cache.is_jwt_blacklisted(jti)
