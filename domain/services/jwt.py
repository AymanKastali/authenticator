from domain.config.config_models import JwtDomainConfig
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.interfaces.policy import PolicyInterface
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_type import JwtTypeVo


class JwtDomainService:
    """Pure domain JWT logic, independent of framework or async."""

    def __init__(
        self,
        jwt_service: JwtServicePort,
        jwt_redis_repo: JwtRedisRepositoryPort,
        config: JwtDomainConfig,
        policies: list[PolicyInterface],
    ):
        self._jwt_service = jwt_service
        self._jwt_redis_repo = jwt_redis_repo
        self._config = config
        self._policies = policies

    # ------------------------- Payload Creation -------------------------
    def _create_payload(
        self, user: UserEntity, token_type: JwtTypeVo, exp_seconds: int
    ) -> JwtPayloadVo:
        """Create a JWT payload (value object)."""
        return JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=token_type,
            roles=user.roles,
            exp=exp_seconds,
            iss=self._config.issuer,
            aud=self._config.audience,
            policies=self._policies,
        )

    # ------------------------- Token Creation -------------------------
    def create_access_token(
        self, user: UserEntity, headers: JwtHeaderVo | None = None
    ) -> str:
        payload_vo = self._create_payload(
            user=user,
            token_type=JwtTypeVo.ACCESS,
            exp_seconds=self._config.access_token_exp_seconds,
        )
        token: JwtEntity = self._jwt_service.sign(payload_vo, headers)
        return token.signature

    def create_refresh_token(
        self, user: UserEntity, headers: JwtHeaderVo | None = None
    ) -> str:
        payload_vo = self._create_payload(
            user=user,
            token_type=JwtTypeVo.REFRESH,
            exp_seconds=self._config.refresh_token_exp_seconds,
        )
        token: JwtEntity = self._jwt_service.sign(payload_vo, headers)
        return token.signature

    # ------------------------- Token Verification -------------------------
    def verify_token(
        self,
        token: str,
        subject: str | None = None,
        expected_headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        """Verify a JWT, including optional header checks."""
        return self._jwt_service.verify(token, subject, expected_headers)

    def verify_refresh_token(
        self,
        token: str,
        subject: str | None = None,
        expected_headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        """Verify a refresh token, including headers and type."""
        payload_vo = self._jwt_service.verify_refresh_token(
            token, subject, expected_headers
        )
        return payload_vo

    # ------------------------- Blacklisting -------------------------
    async def blacklist_token(self, payload: JwtPayloadVo) -> None:
        if not payload.is_expired():
            await self._jwt_redis_repo.blacklist_jwt(payload.jti, payload.exp)

    async def is_jwt_blacklisted(self, jti: UUIDVo) -> bool:
        return await self._jwt_redis_repo.is_jwt_blacklisted(jti)
