from fastapi import Depends

from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from domain.services.user import UserDomainService
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    user_domain_service_dependency,
)


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
