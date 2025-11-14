from fastapi import Depends

from domain.ports.repositories.user import UserRepositoryPort
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.authenticate.register_user import RegisterUser
from domain.services.password.hash import HashPassword
from domain.services.password.verify import VerifyPassword
from presentation.db.in_memory.repositories import get_in_memory_user_repository
from presentation.web.fastapi.api.v1.dependencies.domain.password import (
    password_hasher_dependency,
    password_verifier_dependency,
)


def register_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    hasher: HashPassword = Depends(password_hasher_dependency),
) -> RegisterUser:
    return RegisterUser(user_repo=user_repo, hasher=hasher)


def authenticate_user_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
    verifier: VerifyPassword = Depends(password_verifier_dependency),
) -> AuthenticateUser:
    return AuthenticateUser(user_repo=user_repo, verifier=verifier)
