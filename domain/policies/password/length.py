from domain.config import password_config as pwd_cfg
from domain.exceptions.domain_errors import PolicyViolationError
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.policy_description import PolicyDescriptionVo


class PasswordLengthPolicy(PolicyInterface):
    def __init__(
        self,
        min_length: int = pwd_cfg.min_length,
        max_length: int = pwd_cfg.max_length,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def enforce(self, target: str) -> None:
        if not isinstance(target, str):
            raise PolicyViolationError(
                "Password must be a string.", policy_name="length_type"
            )

        if len(target) < self.min_length:
            raise PolicyViolationError(
                f"Password too short. Minimum {self.min_length} characters.",
                policy_name="length_min",
            )
        if len(target) > self.max_length:
            raise PolicyViolationError(
                f"Password too long. Maximum {self.max_length} characters.",
                policy_name="length_max",
            )

    def describe(self) -> PolicyDescriptionVo:
        return PolicyDescriptionVo(
            name="length",
            category="password",
            parameters={
                "min_length": self.min_length,
                "max_length": self.max_length,
            },
        )
