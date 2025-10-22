from fastapi import Depends

from application.use_cases.user_use_cases.get_request_user_uc import (
    GetRequestUserUseCase,
)
from delivery.db.in_memory.repositories import (
    get_in_memory_user_repository,
)


def get_request_user_use_case(
    user_repo=Depends(get_in_memory_user_repository),
) -> GetRequestUserUseCase:
    return GetRequestUserUseCase(user_repo=user_repo)
