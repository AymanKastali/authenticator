from fastapi import Depends

from domain.ports.repositories.user import UserRepositoryPort
from domain.services.password import PasswordDomainService
from domain.services.user.authenticate_user import AuthenticateUser
from domain.services.user.query_user import QueryUser
from domain.services.user.register_user import RegisterUser
from presentation.db.in_memory.repositories import get_in_memory_user_repository
from presentation.web.fastapi.api.v1.dependencies.domain.password import (
    password_domain_service_dependency,
)


def register_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    password_service: PasswordDomainService = Depends(
        password_domain_service_dependency
    ),
) -> RegisterUser:
    return RegisterUser(user_repo=user_repo, password_service=password_service)


def authenticate_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> AuthenticateUser:
    return AuthenticateUser(user_repo=user_repo)


def query_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> QueryUser:
    return QueryUser(user_repo=user_repo)
