from application.services.policy import PolicyService
from presentation.web.fastapi.api.v1.dependencies.domain.policy import (
    jwt_policies,
    password_policies,
)


def policy_service_dependency() -> PolicyService:
    policies = jwt_policies() + password_policies()
    return PolicyService(policies)
