from domain.config import password_config as pwd_cfg
from domain.exceptions.domain_errors import PasswordError
from domain.interfaces.password_policy import PasswordPolicyInterface
from domain.value_objects.policy_description import PolicyDescriptionVo


class PasswordLengthPolicy(PasswordPolicyInterface):
    def __init__(
        self,
        min_length: int = pwd_cfg.min_length,
        max_length: int = pwd_cfg.max_length,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def enforce(self, password: str) -> None:
        if not isinstance(password, str):
            raise PasswordError("Password must be a string.")

        if len(password) < self.min_length:
            raise PasswordError(
                f"Password too short. Minimum {self.min_length} characters."
            )
        if len(password) > self.max_length:
            raise PasswordError(
                f"Password too long. Maximum {self.max_length} characters."
            )

    def describe(self) -> PolicyDescriptionVo:
        return PolicyDescriptionVo(
            name="length",
            type="password",
            parameters={
                "min_length": self.min_length,
                "max_length": self.max_length,
            },
        )
