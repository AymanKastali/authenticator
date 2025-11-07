from fastapi import Depends

from application.services.auth.authentication import AuthService
from application.use_cases.auth.registration.register import RegisterUserUseCase
from domain.services.password import PasswordDomainService
from domain.services.user import UserDomainService
from presentation.web.fastapi.api.v1.dependencies.domain.password import (
    password_domain_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    user_domain_service_dependency,
)


# Services
def auth_service_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
) -> AuthService:
    return AuthService(user_service)


# Use Cases
def register_user_uc_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
    password_service: PasswordDomainService = Depends(
        password_domain_service_dependency
    ),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(user_service, password_service)
