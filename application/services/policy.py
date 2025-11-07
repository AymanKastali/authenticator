from application.dto.policies.app import PolicyDescriptionDto
from domain.interfaces.password_policy import PasswordPolicyInterface
from domain.services.password import PasswordDomainService


class PolicyService:
    def __init__(self, password_service: PasswordDomainService):
        self._policies: list[PasswordPolicyInterface] = (
            password_service.policies
        )

    def list(self) -> list[PolicyDescriptionDto]:
        return [
            PolicyDescriptionDto(
                name=policy.describe().name,
                type=policy.describe().type,
                parameters=dict(policy.describe().parameters),
            )
            for policy in self._policies
        ]
