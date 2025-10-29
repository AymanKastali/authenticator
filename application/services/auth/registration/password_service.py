from application.dto.policies.password import PasswordPolicyConfigDto
from domain.policies.password.complexity import PasswordComplexityPolicy
from domain.policies.password.length import PasswordLengthPolicy
from domain.value_objects.hashed_password import HashedPassword


class PasswordService:
    def __init__(self, policy_config: PasswordPolicyConfigDto):
        self._policies = [
            PasswordLengthPolicy(
                min_length=policy_config.min_length,
                max_length=policy_config.max_length,
            ),
            PasswordComplexityPolicy(
                require_upper=policy_config.require_upper,
                require_lower=policy_config.require_lower,
                require_digit=policy_config.require_digit,
                require_special=policy_config.require_special,
            ),
        ]

    def create_hashed_password(self, password: str) -> HashedPassword:
        return HashedPassword.from_plain(password, self._policies)
