from fastapi import Depends

from domain.ports.repositories.user import UserRepositoryPort
from domain.services.user.query_user import QueryUser
from presentation.db.in_memory.repositories import get_in_memory_user_repository


def query_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> QueryUser:
    return QueryUser(user_repo=user_repo)
