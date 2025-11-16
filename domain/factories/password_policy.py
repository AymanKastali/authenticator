from typing import Self

from domain.interfaces.policy import PolicyInterface
from domain.interfaces.policy_builder import PolicyBuilderInterface
from domain.policies.password.complexity import PasswordComplexityPolicy
from domain.policies.password.length import PasswordLengthPolicy


class PasswordPolicyBuilder(PolicyBuilderInterface):
    """Builder for assembling password policies."""

    def __init__(self) -> None:
        self._policies: list[PolicyInterface] = []

    def add_policy(self, policy: PolicyInterface) -> Self:
        self._policies.append(policy)
        return self

    def add_length_policy(
        self, *, min_length: int = 8, max_length: int = 128
    ) -> Self:
        policy = PasswordLengthPolicy(
            min_length=min_length, max_length=max_length
        )
        self._policies.append(policy)
        return self

    def add_complexity_policy(
        self,
        *,
        require_upper: bool = True,
        require_lower: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
    ) -> Self:
        policy = PasswordComplexityPolicy(
            require_upper=require_upper,
            require_lower=require_lower,
            require_digit=require_digit,
            require_special=require_special,
        )
        self._policies.append(policy)
        return self

    def build(self) -> list[PolicyInterface]:
        return self._policies
