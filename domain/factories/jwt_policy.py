from typing import Self

from domain.interfaces.policy import PolicyInterface
from domain.interfaces.policy_builder import PolicyBuilderInterface
from domain.policies.jwt.expiration import JwtExpirationPolicy


class JwtPolicyBuilder(PolicyBuilderInterface):
    """Assemble domain policies from config or custom overrides."""

    def __init__(self) -> None:
        self._policies: list[PolicyInterface] = []

    def add_policy(self, policy: PolicyInterface) -> Self:
        self._policies.append(policy)
        return self

    def add_expiry_policy(
        self,
        *,
        access_token_max_age_seconds: int = 1 * 60 * 60 * 24 * 7,  # 7 days
        refresh_token_max_age_seconds: int = 1 * 60 * 60 * 24 * 30,  # 30 days
    ) -> Self:
        policy = JwtExpirationPolicy(
            access_token_max_age_seconds=access_token_max_age_seconds,
            refresh_token_max_age_seconds=refresh_token_max_age_seconds,
        )
        self._policies.append(policy)
        return self

    def build(self) -> list[PolicyInterface]:
        return self._policies
