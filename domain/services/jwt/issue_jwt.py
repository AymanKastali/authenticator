from domain.config.config_models import JwtDomainConfig
from domain.entities.user import UserEntity
from domain.interfaces.policy import PolicyInterface
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_type import JwtTypeVo


class IssueJwt:
    """Issue new JWTs (access and refresh) for a user."""

    def __init__(
        self,
        jwt_service: JwtServicePort,
        config: JwtDomainConfig,
        policies: list[PolicyInterface],
    ):
        self._jwt_service = jwt_service
        self._config = config
        self._policies = policies

    def access(
        self, user: UserEntity, headers: JwtHeaderVo | None = None
    ) -> str:
        payload = self._create_payload(
            user, JwtTypeVo.ACCESS, self._config.access_token_exp_seconds
        )
        token = self._jwt_service.sign(payload, headers)
        return token.signature

    def refresh(
        self, user: UserEntity, headers: JwtHeaderVo | None = None
    ) -> str:
        payload = self._create_payload(
            user, JwtTypeVo.REFRESH, self._config.refresh_token_exp_seconds
        )
        token = self._jwt_service.sign(payload, headers)
        return token.signature

    def _create_payload(
        self, user: UserEntity, token_type: JwtTypeVo, exp_seconds: int
    ) -> JwtPayloadVo:
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
