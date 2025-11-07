from fastapi import Depends

from application.services.policy import PolicyService
from domain.services.password import PasswordDomainService
from presentation.web.fastapi.api.v1.dependencies.domain.password import (
    password_domain_service_dependency,
)


# Services
def policy_service_dependency(
    password_service: PasswordDomainService = Depends(
        password_domain_service_dependency
    ),
) -> PolicyService:
    return PolicyService(password_service)
