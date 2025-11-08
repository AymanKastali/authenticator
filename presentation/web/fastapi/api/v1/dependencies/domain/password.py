from domain.services.password import PasswordDomainService
from presentation.web.fastapi.api.v1.dependencies.domain.policy import (
    password_policies,
)


def password_domain_service_dependency() -> PasswordDomainService:
    """Provide password service implementation."""
    policies = password_policies()
    return PasswordDomainService(policies)
