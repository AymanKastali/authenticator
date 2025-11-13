import re

from domain.exceptions.domain_errors import (
    PolicyViolationError,
)
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.policy_description import PolicyDescriptionVo


class PasswordComplexityPolicy(PolicyInterface):
    """Validates basic password complexity."""

    def __init__(
        self, require_upper, require_lower, require_digit, require_special
    ):
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special

    def enforce(self, target: str) -> None:
        if self.require_upper and not re.search(r"[A-Z]", target):
            raise PolicyViolationError(
                "Password must contain at least one uppercase letter.",
                policy_name="complexity_upper",
            )
        if self.require_lower and not re.search(r"[a-z]", target):
            raise PolicyViolationError(
                "Password must contain at least one lowercase letter.",
                policy_name="complexity_lower",
            )
        if self.require_digit and not re.search(r"\d", target):
            raise PolicyViolationError(
                "Password must contain at least one digit.",
                policy_name="complexity_digit",
            )
        if self.require_special and not re.search(r"[^A-Za-z0-9]", target):
            raise PolicyViolationError(
                "Password must contain at least one special character.",
                policy_name="complexity_special",
            )

    def describe(self) -> PolicyDescriptionVo:
        return PolicyDescriptionVo(
            name="complexity",
            category="password",
            parameters={
                "require_upper": self.require_upper,
                "require_lower": self.require_lower,
                "require_digit": self.require_digit,
                "require_special": self.require_special,
            },
        )
