from application.dto.policies.app import PolicyDto
from domain.config import domain_config


class PolicyService:
    def __init__(self):
        self._policies: list[PolicyDto] = []

    def list(self) -> list[PolicyDto]:
        policies: list[PolicyDto] = []

        pwd = domain_config.password_config
        policies.append(
            PolicyDto(
                name="length",
                type="password",
                parameters={
                    "min_length": pwd.min_length,
                    "max_length": pwd.max_length,
                },
            )
        )
        policies.append(
            PolicyDto(
                name="complexity",
                type="password",
                parameters={
                    "require_upper": pwd.require_upper,
                    "require_lower": pwd.require_lower,
                    "require_digit": pwd.require_digit,
                    "require_special": pwd.require_special,
                },
            )
        )

        return policies
