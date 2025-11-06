from fastapi import Depends

from application.dto.policies.password import PasswordPolicyConfigDto
from application.ports.services.logger import LoggerPort
from application.services.auth.registration.password_service import (
    PasswordService,
)
from application.use_cases.auth.registration.register import RegisterUserUseCase
from domain.services.user import UserDomainService
from presentation.web.fastapi.api.v1.controllers.auth.registration.register import (
    RegisterUserController,
)
from presentation.web.fastapi.api.v1.dependencies.domain import (
    user_domain_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
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
    user_service: UserDomainService = Depends(user_domain_service_dependency),
    password_service: PasswordService = Depends(password_service_dependency),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(user_service, password_service)


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserController:
    return RegisterUserController(use_case, logger)
