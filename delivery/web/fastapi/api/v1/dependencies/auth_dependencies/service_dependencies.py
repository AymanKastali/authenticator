from fastapi import Depends

from adapters.gateways.authentication.jwt_service import JwtService
from application.ports.jwt_token_service import JwtTokenServicePort
from application.services.auth_session import SessionAuthService
from application.services.authentication import AuthenticationService
from application.services.jwt_auth_service import JwtAuthService
from delivery.bootstrap.domain_config_factory import DomainConfigFactory
from delivery.db.in_memory.repositories import (
    get_in_memory_session_repository,
    get_in_memory_user_repository,
)


def get_jwt_service():
    return JwtService(jwt_cfg=DomainConfigFactory.load_jwt_config())


def get_jwt_auth_service(
    user_repo=Depends(get_in_memory_user_repository),
    jwt_service: JwtTokenServicePort = Depends(get_jwt_service),
) -> JwtAuthService:
    return JwtAuthService(user_repo=user_repo, jwt_service=jwt_service)


def get_session_auth_service(
    user_repo=Depends(get_in_memory_user_repository),
    session_repo=Depends(get_in_memory_session_repository),
) -> SessionAuthService:
    return SessionAuthService(user_repo=user_repo, session_repo=session_repo)


def get_auth_service(
    user_repo=Depends(get_in_memory_user_repository),
) -> AuthenticationService:
    return AuthenticationService(user_repo=user_repo)
