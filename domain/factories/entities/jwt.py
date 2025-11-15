from typing import Any, Mapping

from domain.config.config_models import JwtDomainConfig
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.factories.value_objects.claims import JwtClaimsVoFactory

# Value Object Factories
from domain.factories.value_objects.header import JwtHeaderVoFactory
from domain.factories.value_objects.header_algorithm import (
    JwtHeaderAlgorithmVoFactory,
)
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo

# Value Objects
from domain.value_objects.jwt_status import JwtStatusVo


class JwtEntityFactory(JwtFactoryInterface):
    """
    Factory responsible for constructing JWT entities
    using dedicated VO factories and applying policies.
    """

    def __init__(
        self,
        config: JwtDomainConfig,
        policies: list[PolicyInterface],
    ):
        self._config = config
        self._policies = policies

    # ======================================================
    # PUBLIC API
    # ======================================================

    def create_access_token(self, user: UserEntity) -> JwtEntity:
        claims = self._build_claims(
            user=user,
            token_type="access",
            lifetime_seconds=self._config.access_token_exp_seconds,
        )
        headers = self._build_headers()
        return JwtEntity(
            status=JwtStatusVo.ACTIVE,
            claims=claims,
            headers=headers,
        )

    def create_refresh_token(self, user: UserEntity) -> JwtEntity:
        claims = self._build_claims(
            user=user,
            token_type="refresh",
            lifetime_seconds=self._config.refresh_token_exp_seconds,
        )
        headers = self._build_headers()
        return JwtEntity(
            status=JwtStatusVo.ACTIVE,
            claims=claims,
            headers=headers,
        )

    # ======================================================
    # INTERNAL HELPERS — using VO FACTORIES
    # ======================================================

    def _build_claims(
        self,
        user: UserEntity,
        token_type: str,
        lifetime_seconds: int,
    ) -> JwtClaimsVo:
        # Delegates every detail to the JwtClaimsVoFactory
        claims = JwtClaimsVoFactory.create(
            token_type_str=token_type,
            lifetime_seconds=lifetime_seconds,
            email_str=user.email.value,
            role_strs=[r.value for r in user.roles],
            issuer=self._config.issuer,
            audience=self._config.audience,
        )

        # Apply domain policies
        for policy in self._policies:
            policy.enforce(claims)

        return claims

    def _build_headers(self) -> JwtHeaderVo:
        # Use your algorithm factory → header factory
        alg = JwtHeaderAlgorithmVoFactory.from_string(self._config.algorithm)
        return JwtHeaderVoFactory.create(alg)

    # ======================================================
    # RECONSTRUCTION FROM DECODED DATA
    # ======================================================

    def from_decoded(
        self,
        decoded_claims: Mapping[str, Any],
        decoded_headers: Mapping[str, Any],
    ) -> JwtEntity:
        # Use VO factories to rebuild VOs
        claims_vo = JwtClaimsVoFactory.from_dict(dict(decoded_claims))
        headers_vo = JwtHeaderVoFactory.from_dict(dict(decoded_headers))

        # Re-apply all domain policies
        for policy in self._policies:
            policy.enforce(claims_vo)

        return JwtEntity(
            status=JwtStatusVo.ACTIVE,
            claims=claims_vo,
            headers=headers_vo,
        )
