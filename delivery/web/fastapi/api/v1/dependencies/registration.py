from fastapi import Depends

from adapters.controllers.auth.registration.register import (
    RegisterUserController,
)
from application.dto.policies.password import PasswordPolicyConfigDto
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.logger import LoggerPort
from application.services.auth.registration.password_service import (
    PasswordService,
)
from application.use_cases.auth.registration.register import RegisterUserUseCase
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from delivery.web.fastapi.api.v1.handlers.auth.registration.register import (
    RegisterUserHandler,
)


# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
def password_policy_dependency() -> PasswordPolicyConfigDto:
    """Provide password policy configuration"""
    return PasswordPolicyConfigDto(
        min_length=8,
        max_length=128,
        require_upper=True,
        require_lower=True,
        require_digit=True,
        require_special=True,
    )


# -----------------------------------------------------------------------------
# SERVICES
# -----------------------------------------------------------------------------
def password_service_dependency(
    policy_config: PasswordPolicyConfigDto = Depends(
        password_policy_dependency
    ),
) -> PasswordService:
    """Provide password service implementation"""
    return PasswordService(policy_config=policy_config)


# -----------------------------------------------------------------------------
# USE CASES
# -----------------------------------------------------------------------------
def register_user_uc_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    password_service: PasswordService = Depends(password_service_dependency),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(
        user_repo=user_repo,
        password_service=password_service,
    )


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
) -> RegisterUserController:
    return RegisterUserController(use_case=use_case)


# -----------------------------------------------------------------------------
# HANDLERS
# -----------------------------------------------------------------------------
def register_user_handler_dependency(
    controller: RegisterUserController = Depends(
        register_user_controller_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserHandler:
    return RegisterUserHandler(controller=controller, logger=logger)
