from application.dto.policies.app import PolicyDescriptionDto
from domain.interfaces.policy import PolicyInterface


class PolicyService:
    def __init__(self, policies: list[PolicyInterface]):
        self._policies = policies

    def list(self) -> list[PolicyDescriptionDto]:
        return [
            PolicyDescriptionDto(
                name=policy.describe().name,
                category=policy.describe().category,
                parameters=dict(policy.describe().parameters),
            )
            for policy in self._policies
        ]
