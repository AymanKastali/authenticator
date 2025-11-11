from fastapi import Depends

from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    query_user_dependency,
)


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
