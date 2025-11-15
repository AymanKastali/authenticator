from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from domain.factories.user_factory import UserFactory
from domain.interfaces.user_factory import UserFactoryInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.services.user.query_user import QueryUser
from presentation.web.fastapi.api.v1.controllers.user.get_all import (
    GetAllUsersController,
)
from presentation.web.fastapi.api.v1.controllers.user.get_by_id import (
    GetUserByIdController,
)
from presentation.web.fastapi.dependencies.logger import (
    get_console_json_logger,
)
from presentation.web.fastapi.dependencies.persistence import (
    in_memory_user_repository,
)


# Domain
def user_factory_dependency() -> UserFactoryInterface:
    return UserFactory()


def query_user_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
) -> QueryUser:
    return QueryUser(user_repo=user_repo)


# Application
def get_user_by_id_uc_dependency(
    query_user=Depends(query_user_dependency),
) -> GetUserByIdUseCase:
    """Provide use case for registering a user"""
    return GetUserByIdUseCase(query_user)


def get_user_all_users_uc_dependency(
    query_user=Depends(query_user_dependency),
) -> GetAllUsersUseCase:
    """Provide use case for registering a user"""
    return GetAllUsersUseCase(query_user)


# Presentation
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
