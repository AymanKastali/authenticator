from fastapi import Depends

from application.ports.repositories.session import SessionRepositoryPort
from application.services.auth.session import SessionAuthService
from presentation.db.in_memory.repositories import (
    get_in_memory_session_repository,
)
from presentation.web.fastapi.api.v1.controllers.auth.session.login import (
    SessionLoginController,
)


# Application
def session_auth_service_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
    session_repo: SessionRepositoryPort = Depends(
        get_in_memory_session_repository
    ),
) -> SessionAuthService:
    return SessionAuthService(user_service, session_repo)


# Presentation
def session_auth_controller_dependency(
    service: SessionAuthService = Depends(session_auth_service_dependency),
) -> SessionLoginController:
    return SessionLoginController(service)
