from fastapi import Depends

from application.services.auth_jwt import JwtAuthService
from application.services.auth_session import SessionAuthService
from application.use_cases.jwt_login import JwtLoginUseCase
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.session_login import SessionLoginUseCase
from delivery.db.in_memory.repositories import (
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.service_dependencies import (
    get_jwt_auth_service,
    get_session_auth_service,
)


def get_jwt_login_uc(
    jwt_auth_service: JwtAuthService = Depends(get_jwt_auth_service),
) -> JwtLoginUseCase:
    return JwtLoginUseCase(jwt_auth_service)


def get_session_login_uc(
    session_auth_service: SessionAuthService = Depends(
        get_session_auth_service
    ),
) -> SessionLoginUseCase:
    return SessionLoginUseCase(session_auth_service)


def get_register_user_uc(
    user_repo=Depends(get_in_memory_user_repository),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo)
