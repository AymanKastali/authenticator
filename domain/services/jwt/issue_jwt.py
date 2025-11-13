from domain.config.config_models import JwtDomainConfig
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.interfaces.policy import PolicyInterface
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo
from domain.value_objects.jwt_type import JwtTypeVo


class IssueJwt:
    def __init__(
        self,
        jwt_service: JwtServicePort,
        config: JwtDomainConfig,
        policies: list[PolicyInterface],
    ):
        self._jwt_service = jwt_service
        self._config = config
        self._policies = policies

    def issue_access_token(self, user: UserEntity) -> str:
        claims: JwtClaimsVo = self._create_claims(
            user, JwtTypeVo.ACCESS, self._config.access_token_exp_seconds
        )
        headers: JwtHeaderVo = self._create_headers()
        token: JwtEntity = JwtEntity.create(claims=claims, headers=headers)
        return self._jwt_service.sign_token(token)

    def issue_refresh_token(self, user: UserEntity) -> str:
        claims: JwtClaimsVo = self._create_claims(
            user, JwtTypeVo.REFRESH, self._config.refresh_token_exp_seconds
        )
        headers: JwtHeaderVo = self._create_headers()
        token: JwtEntity = JwtEntity.create(claims=claims, headers=headers)
        return self._jwt_service.sign_token(token)

    def _create_claims(
        self, user: UserEntity, token_type: JwtTypeVo, lifetime_seconds: int
    ) -> JwtClaimsVo:
        return JwtClaimsVo.create(
            sub=user.uid,
            email=user.email,
            typ=token_type,
            roles=user.roles,
            lifetime_seconds=lifetime_seconds,
            iss=self._config.issuer,
            aud=self._config.audience,
            policies=self._policies,
        )

    def _create_headers(self) -> JwtHeaderVo:
        """Create default headers based on config."""
        return JwtHeaderVo.create(
            alg=JwtHeaderAlgorithmVo.from_string(self._config.algorithm)
        )
