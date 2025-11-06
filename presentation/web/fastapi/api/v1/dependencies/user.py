from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from domain.services.user import UserDomainService
from presentation.web.fastapi.api.v1.controllers.user.get_all import (
    GetAllUsersController,
)
from presentation.web.fastapi.api.v1.controllers.user.get_by_id import (
    GetUserByIdController,
)
from presentation.web.fastapi.api.v1.dependencies.domain import (
    user_domain_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)


# -----------------------------------------------------------------------------
# USE CASES
# -----------------------------------------------------------------------------
def get_user_by_id_uc_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
) -> GetUserByIdUseCase:
    """Provide use case for registering a user"""
    return GetUserByIdUseCase(user_service)


def get_user_all_users_uc_dependency(
    user_service: UserDomainService = Depends(user_domain_service_dependency),
) -> GetAllUsersUseCase:
    """Provide use case for registering a user"""
    return GetAllUsersUseCase(user_service)


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
def get_user_by_id_controller_dependency(
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> GetUserByIdController:
    """Provide use case for registering a user"""
    return GetUserByIdController(use_case, logger)


def get_user_all_users_controller_dependency(
    use_case: GetAllUsersUseCase = Depends(get_user_all_users_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> GetAllUsersController:
    """Provide use case for registering a user"""
    return GetAllUsersController(use_case, logger)
