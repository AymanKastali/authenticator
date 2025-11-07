from fastapi import Depends

from application.services.auth.session import SessionAuthService
from presentation.web.fastapi.api.v1.controllers.auth.session.login import (
    SessionLoginController,
)
from presentation.web.fastapi.api.v1.dependencies.application.session import (
    session_auth_service_dependency,
)


def session_auth_controller_dependency(
    service: SessionAuthService = Depends(session_auth_service_dependency),
) -> SessionLoginController:
    return SessionLoginController(service)
