from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from presentation.web.fastapi.api.v1.controllers.user.get_all import (
    GetAllUsersController,
)
from presentation.web.fastapi.api.v1.controllers.user.get_by_id import (
    GetUserByIdController,
)
from presentation.web.fastapi.api.v1.dependencies.application.user import (
    get_user_all_users_uc_dependency,
    get_user_by_id_uc_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.logger import (
    get_console_json_logger,
)


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
