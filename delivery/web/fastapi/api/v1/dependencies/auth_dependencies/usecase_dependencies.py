from fastapi import Depends

from adapters.gateways.authentication.jwt_service import JwtService
from application.use_cases.login_user_use_case import LoginUserUseCase
from delivery.db.in_memory.user_repository import get_in_memory_repository
from domain.interfaces.user import IUserRepository
from domain.services.authentication import AuthenticationService


def get_authentication_service(
    repo: IUserRepository = Depends(get_in_memory_repository),
) -> AuthenticationService:
    return AuthenticationService(repo)


def get_jwt_service() -> JwtService:
    # Secret and expiration can come from config/env
    return JwtService(secret="supersecretkey", expiration_minutes=60)


def get_login_user_use_case(
    auth_service: AuthenticationService = Depends(get_authentication_service),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> LoginUserUseCase:
    return LoginUserUseCase(auth_service, jwt_service)
