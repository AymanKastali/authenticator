from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.auth.register.register_user import (
    RegisterUserUseCase,
)
from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.user_factory import UserEntityFactoryInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.authenticate.register_user import RegisterUser
from presentation.web.fastapi.api.v1.controllers.auth.registration.register import (
    RegisterUserController,
)
from presentation.web.fastapi.dependencies.logger import (
    get_console_json_logger,
)

# from presentation.web.fastapi.dependencies.password import (
#     password_hasher_dependency,
#     password_verifier_dependency,
# )
from presentation.web.fastapi.dependencies.password import (
    pwdlib_hasher_dependency,
)
from presentation.web.fastapi.dependencies.persistence import (
    in_memory_user_repository,
)
from presentation.web.fastapi.dependencies.policy import password_policies
from presentation.web.fastapi.dependencies.user import (
    user_entity_factory_dependency,
)


# Domain
def register_user_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
    user_factory: UserEntityFactoryInterface = Depends(
        user_entity_factory_dependency
    ),
    hasher: PasswordHasherInterface = Depends(pwdlib_hasher_dependency),
) -> RegisterUser:
    policies: list[PolicyInterface] = password_policies()
    return RegisterUser(
        user_repo=user_repo,
        user_factory=user_factory,
        hasher=hasher,
        policies=policies,
    )


def authenticate_user_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
    password_hasher: PasswordHasherInterface = Depends(
        pwdlib_hasher_dependency
    ),
) -> AuthenticateUser:
    return AuthenticateUser(
        user_repo=user_repo, password_hasher=password_hasher
    )


# Application
def register_user_uc_dependency(
    registration: RegisterUser = Depends(register_user_dependency),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(registration)


# Presentation
def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserController:
    return RegisterUserController(use_case, logger)
