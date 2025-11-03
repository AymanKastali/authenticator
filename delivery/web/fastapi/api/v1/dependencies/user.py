from fastapi import Depends

from adapters.controllers.user.get_all import GetAllUsersController
from adapters.controllers.user.get_by_id import GetUserByIdController
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from delivery.web.fastapi.api.v1.handlers.user.get_all import GetAllUsersHandler
from delivery.web.fastapi.api.v1.handlers.user.get_by_id import (
    GetUserByIdHandler,
)


# -----------------------------------------------------------------------------
# USE CASES
# -----------------------------------------------------------------------------
def get_user_by_id_uc_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> GetUserByIdUseCase:
    """Provide use case for registering a user"""
    return GetUserByIdUseCase(user_repo=user_repo)


def get_user_all_users_uc_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> GetAllUsersUseCase:
    """Provide use case for registering a user"""
    return GetAllUsersUseCase(user_repo=user_repo)


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def get_user_by_id_controller_dependency(
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_uc_dependency),
) -> GetUserByIdController:
    """Provide use case for registering a user"""
    return GetUserByIdController(use_case)


def get_user_all_users_controller_dependency(
    use_case: GetAllUsersUseCase = Depends(get_user_all_users_uc_dependency),
) -> GetAllUsersController:
    """Provide use case for registering a user"""
    return GetAllUsersController(use_case)


# -----------------------------------------------------------------------------
# HANDLERS
# -----------------------------------------------------------------------------
def get_user_by_id_handler_dependency(
    controller: GetUserByIdController = Depends(
        get_user_by_id_controller_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> GetUserByIdHandler:
    """Provide use case for registering a user"""
    return GetUserByIdHandler(controller, logger)


def get_user_all_users_handler_dependency(
    controller: GetAllUsersController = Depends(
        get_user_all_users_controller_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> GetAllUsersHandler:
    """Provide use case for registering a user"""
    return GetAllUsersHandler(controller, logger)
