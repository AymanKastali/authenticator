from fastapi import Depends

from application.ports.repositories.session import SessionRepositoryPort
from application.services.auth.session import SessionAuthService
from domain.services.user import UserDomainService
from presentation.db.in_memory.repositories import (
    get_in_memory_session_repository,
)
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    user_domain_service_dependency,
)


def session_auth_service_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
    session_repo: SessionRepositoryPort = Depends(
        get_in_memory_session_repository
    ),
) -> SessionAuthService:
    return SessionAuthService(user_service, session_repo)
