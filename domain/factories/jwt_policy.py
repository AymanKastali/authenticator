from typing import Self

from domain.config.config_models import JwtDomainConfig
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.policy_builder import PolicyBuilderInterface
from domain.policies.jwt.expiration import JwtExpirationPolicy


class JwtPolicyBuilder(PolicyBuilderInterface):
    """Assemble domain policies from config or custom overrides."""

    def __init__(self, config: JwtDomainConfig):
        self._config = config
        self._policies: list[PolicyInterface] = []

    def add_policy(self, policy: PolicyInterface) -> Self:
        self._policies.append(policy)
        return self

    def add_expiry_policy(
        self,
        *,
        access_token_expiry_seconds: int | None = None,
        refresh_token_expiry_seconds: int | None = None,
    ) -> Self:
        access_exp = (
            access_token_expiry_seconds
            if access_token_expiry_seconds
            else self._config.access_token_exp_seconds
        )
        refresh_exp = (
            refresh_token_expiry_seconds
            if refresh_token_expiry_seconds
            else self._config.refresh_token_exp_seconds
        )
        policy = JwtExpirationPolicy(
            access_token_max_age_seconds=access_exp,
            refresh_token_max_age_seconds=refresh_exp,
        )
        self._policies.append(policy)
        return self

    def build(self) -> list[PolicyInterface]:
        return self._policies
