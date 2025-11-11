from fastapi import Depends

from domain.ports.repositories.user import UserRepositoryPort
from domain.services.user.authenticate_user import AuthenticateUser
from domain.services.user.query_user import QueryUser
from domain.services.user.register_user import RegisterUser
from presentation.db.in_memory.repositories import get_in_memory_user_repository
from presentation.web.fastapi.api.v1.dependencies.domain.policy import (
    password_policies,
)


def register_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> RegisterUser:
    policies = password_policies()
    return RegisterUser(user_repo=user_repo, password_policies=policies)


def authenticate_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> AuthenticateUser:
    return AuthenticateUser(user_repo=user_repo)


def query_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> QueryUser:
    return QueryUser(user_repo=user_repo)
