from typing import Self

from domain.config.config_models import PasswordConfig
from domain.interfaces.password_policy import PasswordPolicyInterface
from domain.policies.password.complexity import PasswordComplexityPolicy
from domain.policies.password.length import PasswordLengthPolicy


class PasswordPolicyBuilder:
    """Builder for assembling password policies."""

    def __init__(self):
        self._config: PasswordConfig | None = None
        self._policies: list[PasswordPolicyInterface] = []

    def with_config(self, config: PasswordConfig) -> Self:
        self._config = config
        return self

    def add_length_policy(
        self, *, min_length: int | None = None, max_length: int | None = None
    ) -> Self:
        cfg = self._config or PasswordConfig()
        policy = PasswordLengthPolicy(
            min_length=min_length if min_length is not None else cfg.min_length,
            max_length=max_length if max_length is not None else cfg.max_length,
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
        cfg = self._config or PasswordConfig()
        policy = PasswordComplexityPolicy(
            require_upper=require_upper
            if require_upper is not None
            else cfg.require_upper,
            require_lower=require_lower
            if require_lower is not None
            else cfg.require_lower,
            require_digit=require_digit
            if require_digit is not None
            else cfg.require_digit,
            require_special=require_special
            if require_special is not None
            else cfg.require_special,
        )
        self._policies.append(policy)
        return self

    def build(self) -> list[PasswordPolicyInterface]:
        """Return the assembled password policies, auto-adding from config if none specified."""
        if not self._policies and self._config:
            self.add_length_policy()
            self.add_complexity_policy()
        return self._policies
