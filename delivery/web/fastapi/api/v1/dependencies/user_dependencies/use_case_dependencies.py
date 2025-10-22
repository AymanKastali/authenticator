from fastapi import Depends

from application.use_cases.user_use_cases.get_all_users_uc import (
    GetAllUsersUseCase,
)
from application.use_cases.user_use_cases.get_user_by_id_uc import (
    GetUserByIdUseCase,
)
from application.use_cases.user_use_cases.get_user_me_uc import GetUserMeUseCase
from delivery.db.in_memory.repositories import (
    get_in_memory_user_repository,
)


def get_get_user_by_id_uc(
    user_repo=Depends(get_in_memory_user_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_repo=user_repo)


def get_get_all_users_uc(
    user_repo=Depends(get_in_memory_user_repository),
) -> GetAllUsersUseCase:
    return GetAllUsersUseCase(user_repo=user_repo)


def get_get_user_me_uc(
    user_repo=Depends(get_in_memory_user_repository),
) -> GetUserMeUseCase:
    return GetUserMeUseCase(user_repo=user_repo)
