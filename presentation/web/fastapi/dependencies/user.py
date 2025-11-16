from fastapi import Depends

from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.logger import LoggerPort
from application.repositories.user import UserRepository
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from domain.factories.entities.user import UserEntityFactory
from domain.interfaces.user_factory import UserEntityFactoryInterface
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
def user_entity_factory_dependency() -> UserEntityFactoryInterface:
    return UserEntityFactory()


def user_repo_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
) -> UserRepository:
    return UserRepository(user_repo=user_repo)


# Application
def get_user_by_id_uc_dependency(
    user_repo=Depends(user_repo_dependency),
) -> GetUserByIdUseCase:
    """Provide use case for registering a user"""
    return GetUserByIdUseCase(user_repo)


def get_user_all_users_uc_dependency(
    user_repo=Depends(user_repo_dependency),
) -> GetAllUsersUseCase:
    """Provide use case for registering a user"""
    return GetAllUsersUseCase(user_repo)


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
