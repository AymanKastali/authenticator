from uuid import UUID

from application.dto.auth.jwt.auth_user import AuthUserDto
from application.dto.auth.jwt.token import JwtDto
from application.dto.auth.jwt.tokens import JwtTokensDto
from application.dto.auth.jwt.tokens_config import TokensConfigDto
from application.mappers.jwt import JwtMapper
from application.mappers.user import UserMapper
from application.ports.cache.redis.jwt_blacklist import (
    AsyncJwtBlacklistRedisPort,
)
from application.ports.services.jwt import JwtServicePort
from application.services.auth.authentication import AuthService
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_type import JwtTypeVo


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
        self, user: UserEntity, token_type: JwtTypeVo, exp_seconds: int
    ) -> JwtDto:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=token_type,
            roles=list(user.roles),
            expires_after_seconds=exp_seconds,
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
            token_type=JwtTypeVo.ACCESS,
            exp_seconds=self._tokens_config.access_token_exp,
        )

    def _create_refresh_token(self, user: UserEntity) -> JwtDto:
        return self._create_token(
            user=user,
            token_type=JwtTypeVo.REFRESH,
            exp_seconds=self._tokens_config.refresh_token_exp,
        )

    def _create_tokens(self, user: UserEntity) -> JwtTokensDto:
        access_token: JwtDto = self._create_access_token(user)
        refresh_token: JwtDto = self._create_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token.signature,
            refresh_token=refresh_token.signature,
        )

    async def login(self, email: str, password: str) -> JwtTokensDto:
        dto: AuthUserDto = await self._auth_service.authenticate_user(
            email, password
        )
        user: UserEntity = UserMapper.to_entity_from_auth_user_dto(dto)
        if user.deleted:
            raise ValueError("Deleted")
        return self._create_tokens(user)

    async def logout(self, token: str) -> None:
        dto: JwtDto = self._jwt_service.verify(token)
        token_entity: JwtEntity = JwtMapper.to_entity_from_jwt_dto(dto)
        payload_vo: JwtPayloadVo = token_entity.payload

        if not payload_vo.is_expired():
            expire_at_ts: int = int(payload_vo.exp.to_timestamp())
            await self._blacklist_cache.blacklist_jwt(
                jti=token_entity.jti, expire_at=expire_at_ts
            )

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtDto:
        """Verify a token and return the full DTO."""
        jwt_dto: JwtDto = self._jwt_service.verify(token, subject)
        jwt_entity: JwtEntity = JwtMapper.to_entity_from_jwt_dto(jwt_dto)
        return JwtMapper.to_jwt_dto_from_entity(jwt_entity)

    def verify_refresh_token(self, token: str) -> JwtDto:
        """Verify a refresh token and return the full DTO."""
        jwt_dto: JwtDto = self._jwt_service.verify_refresh_token(token)
        jwt_entity: JwtEntity = JwtMapper.to_entity_from_jwt_dto(jwt_dto)
        return JwtMapper.to_jwt_dto_from_entity(jwt_entity)

    async def refresh_jwt_token(self, refresh_token: str) -> JwtTokensDto:
        token_dto: JwtDto = self.verify_refresh_token(refresh_token)
        user_id = token_dto.payload.sub
        dto: AuthUserDto = await self._auth_service.get_user_by_id(
            UUID(user_id)
        )
        user: UserEntity = UserMapper.to_entity_from_auth_user_dto(dto)
        return self._create_tokens(user)

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        return await self._blacklist_cache.is_jwt_blacklisted(jti)
