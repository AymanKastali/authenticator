from typing import Any, Mapping

from domain.config.config_models import JwtDomainConfig
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo
from domain.value_objects.jwt_status import JwtStatusVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.uuid_id import UUIDVo


class JwtFactory(JwtFactoryInterface):
    """Factory responsible for constructing JWT entities with all invariants."""

    def __init__(
        self, config: JwtDomainConfig, policies: list[PolicyInterface]
    ):
        self._config = config
        self._policies = policies

    def create_access_token(self, user: UserEntity) -> JwtEntity:
        claims = self._build_claims(
            user, JwtTypeVo.ACCESS, self._config.access_token_exp_seconds
        )
        headers = self._build_headers()
        return JwtEntity(
            status=JwtStatusVo.ACTIVE, claims=claims, headers=headers
        )

    def create_refresh_token(self, user: UserEntity) -> JwtEntity:
        claims = self._build_claims(
            user, JwtTypeVo.REFRESH, self._config.refresh_token_exp_seconds
        )
        headers = self._build_headers()
        return JwtEntity(
            status=JwtStatusVo.ACTIVE, claims=claims, headers=headers
        )

    # ----------------- Internal helpers -----------------
    def _build_claims(
        self, user: UserEntity, token_type: JwtTypeVo, lifetime_seconds: int
    ) -> JwtClaimsVo:
        now = DateTimeVo.now()
        jti = UUIDVo.new()
        exp = now.expires_after(seconds=lifetime_seconds)
        nbf = now
        claims = JwtClaimsVo(
            sub=user.uid,
            typ=token_type,
            exp=exp,
            jti=jti,
            iat=now,
            nbf=nbf,
            email=user.email,
            roles=user.roles,
            iss=self._config.issuer,
            aud=self._config.audience,
            extras={},
            username=None,
        )
        # Apply all policies
        for policy in self._policies:
            policy.enforce(claims)
        return claims

    def _build_headers(self) -> JwtHeaderVo:
        return JwtHeaderVo(
            alg=JwtHeaderAlgorithmVo.from_string(self._config.algorithm)
        )

    # ----------------- From Decoded -----------------
    def from_decoded(
        self,
        decoded_claims: Mapping[str, Any],
        decoded_headers: Mapping[str, Any],
    ) -> JwtEntity:
        """
        Reconstruct a JWT entity from decoded data (infra layer),
        enforcing all domain invariants and policies.
        """
        claims_vo = JwtClaimsVo.from_dict(dict(decoded_claims))
        headers_vo = JwtHeaderVo.from_dict(dict(decoded_headers))

        # Apply policies if needed
        for policy in self._policies:
            policy.enforce(claims_vo)

        return JwtEntity(
            status=JwtStatusVo.ACTIVE, claims=claims_vo, headers=headers_vo
        )
