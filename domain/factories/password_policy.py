from typing import Self

from domain.config.config_models import PasswordDomainConfig
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.policy_builder import PolicyBuilderInterface
from domain.policies.password.complexity import PasswordComplexityPolicy
from domain.policies.password.length import PasswordLengthPolicy


class PasswordPolicyBuilder(PolicyBuilderInterface):
    """Builder for assembling password policies."""

    def __init__(self, config: PasswordDomainConfig):
        self._config = config
        self._policies: list[PolicyInterface] = []

    def add_policy(self, policy: PolicyInterface) -> Self:
        self._policies.append(policy)
        return self

    def add_length_policy(
        self, *, min_length: int | None = None, max_length: int | None = None
    ) -> Self:
        minimum_length = min_length if min_length else self._config.min_length
        maximum_length = max_length if max_length else self._config.max_length

        policy = PasswordLengthPolicy(
            min_length=minimum_length, max_length=maximum_length
        )
        self._policies.append(policy)
        return self

    def add_complexity_policy(
        self,
        *,
        require_upper: bool | None = None,
        require_lower: bool | None = None,
        require_digit: bool | None = None,
        require_special: bool | None = None,
    ) -> Self:
        require_uppercase = (
            require_upper if require_upper else self._config.require_upper
        )
        require_lowercase = (
            require_lower if require_lower else self._config.require_lower
        )
        require_digit_number = (
            require_digit if require_digit else self._config.require_digit
        )
        require_special_character = (
            require_special if require_special else self._config.require_special
        )

        policy = PasswordComplexityPolicy(
            require_upper=require_uppercase,
            require_lower=require_lowercase,
            require_digit=require_digit_number,
            require_special=require_special_character,
        )
        self._policies.append(policy)
        return self

    def build(self) -> list[PolicyInterface]:
        return self._policies
