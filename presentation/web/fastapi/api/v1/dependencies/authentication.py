from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.auth.register.register_user import (
    RegisterUserUseCase,
)
from domain.ports.repositories.user import UserRepositoryPort
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.authenticate.register_user import RegisterUser
from domain.services.password.hash import HashPassword
from domain.services.password.verify import VerifyPassword
from presentation.db.in_memory.repositories import get_in_memory_user_repository
from presentation.web.fastapi.api.v1.controllers.auth.registration.register import (
    RegisterUserController,
)
from presentation.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from presentation.web.fastapi.api.v1.dependencies.password import (
    password_hasher_dependency,
    password_verifier_dependency,
)


# Domain
def register_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    hasher: HashPassword = Depends(password_hasher_dependency),
) -> RegisterUser:
    return RegisterUser(user_repo=user_repo, hasher=hasher)


def authenticate_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    verifier: VerifyPassword = Depends(password_verifier_dependency),
) -> AuthenticateUser:
    return AuthenticateUser(user_repo=user_repo, verifier=verifier)


# Application
def register_user_uc_dependency(
    registration: RegisterUser = Depends(register_user_dependency),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(registration)


# Presentation
def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserController:
    return RegisterUserController(use_case, logger)
