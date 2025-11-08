from fastapi import Depends

from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from domain.services.jwt import JwtDomainService
from domain.services.user import UserDomainService
from presentation.web.fastapi.api.v1.dependencies.application.auth import (
    auth_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.jwt import (
    jwt_domain_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    user_domain_service_dependency,
)


# Services
def jwt_auth_service_dependency(
    jwt_service: JwtDomainService = Depends(jwt_domain_service_dependency),
    auth_service: AuthService = Depends(auth_service_dependency),
) -> JwtAuthService:
    return JwtAuthService(jwt_service=jwt_service, auth_service=auth_service)


# Use Cases
def get_authenticated_user_uc_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
) -> GetAuthenticatedUserUseCase:
    """Provide use case for retrieving the authenticated user."""
    return GetAuthenticatedUserUseCase(user_service)
