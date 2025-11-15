from fastapi import Depends

from application.services.auth.session import SessionAuthService
from domain.ports.repositories.session import SessionRepositoryPort
from presentation.web.fastapi.api.v1.controllers.auth.session.login import (
    SessionLoginController,
)
from presentation.web.fastapi.dependencies.persistence import (
    in_memory_session_repository,
)


# Application
def session_auth_service_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
    session_repo: SessionRepositoryPort = Depends(in_memory_session_repository),
) -> SessionAuthService:
    return SessionAuthService(user_service, session_repo)


# Presentation
def session_auth_controller_dependency(
    service: SessionAuthService = Depends(session_auth_service_dependency),
) -> SessionLoginController:
    return SessionLoginController(service)
