from fastapi import Depends

from adapters.controllers.auth.session.login import (
    SessionLoginController,
)
from application.ports.repositories.session import SessionRepositoryPort
from application.ports.repositories.user import UserRepositoryPort
from application.services.auth.session import SessionAuthService
from delivery.db.in_memory.repositories import (
    get_in_memory_session_repository,
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.handlers.auth.session.login import (
    SessionLoginHandler,
)


# -----------------------------------------------------------------------------
# SERVICES
# -----------------------------------------------------------------------------
def session_auth_service_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    session_repo: SessionRepositoryPort = Depends(
        get_in_memory_session_repository
    ),
) -> SessionAuthService:
    return SessionAuthService(user_repo, session_repo)


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def session_auth_controller_dependency(
    service: SessionAuthService = Depends(session_auth_service_dependency),
) -> SessionLoginController:
    return SessionLoginController(service)


# -----------------------------------------------------------------------------
# HANDLERS
# -----------------------------------------------------------------------------
def session_auth_handler_dependency(
    controller: SessionLoginController = Depends(
        session_auth_controller_dependency
    ),
) -> SessionLoginHandler:
    return SessionLoginHandler(controller)
