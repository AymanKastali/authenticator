from domain.config.config_models import JwtConfig
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_type import JwtTypeVo


class JWTDomainService:
    """Pure domain JWT logic, independent of framework or async."""

    def __init__(
        self,
        jwt_service: JwtServicePort,
        jwt_redis_repo: JwtRedisRepositoryPort,
        config: JwtConfig,
    ):
        self._jwt_service = jwt_service
        self._jwt_redis_repo = jwt_redis_repo
        self._config = config

    def _create_payload(
        self, user: UserEntity, token_type: JwtTypeVo, exp_seconds: int
    ) -> JwtPayloadVo:
        """Create a JWT payload (value object)."""
        return JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=token_type,
            roles=user.roles,
            expires_after_seconds=exp_seconds,
            iss=self._config.issuer,
            aud=self._config.audience,
        )

    def create_access_token(self, user: UserEntity) -> str:
        payload_vo: JwtPayloadVo = self._create_payload(
            user=user,
            token_type=JwtTypeVo.ACCESS,
            exp_seconds=self._config.access_token_exp_seconds,
        )
        token: JwtEntity = self._jwt_service.sign(payload_vo)
        return token.signature

    def create_refresh_token(self, user: UserEntity) -> str:
        payload_vo: JwtPayloadVo = self._create_payload(
            user=user,
            token_type=JwtTypeVo.REFRESH,
            exp_seconds=self._config.refresh_token_exp_seconds,
        )
        token: JwtEntity = self._jwt_service.sign(payload_vo)
        return token.signature

    def verify_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadVo:
        """Verify and return a JWT payload value object."""

        return self._jwt_service.verify(token, subject)

    def verify_refresh_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadVo:
        """Verify a refresh token and return the full DTO."""
        return self._jwt_service.verify_refresh_token(token, subject)

    async def blacklist_token(self, payload: JwtPayloadVo) -> None:
        if not payload.is_expired():
            await self._jwt_redis_repo.blacklist_jwt(payload.jti, payload.exp)

    async def is_jwt_blacklisted(self, jti: UUIDVo) -> bool:
        return await self._jwt_redis_repo.is_jwt_blacklisted(jti)

    # def list_policies(self) -> List[PolicyDescriptionVo]:
    #     """Return JWT-related policies (expiration, etc)."""
    #     return [
    #         PolicyDescriptionVo(
    #             name="expiration",
    #             type="jwt",
    #             parameters={"max_age_seconds": 3600},
    #         )
    #     ]
