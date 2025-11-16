from fastapi import Depends

from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.logger import LoggerPort
from application.use_cases.auth.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.use_cases.auth.register_user import RegisterUserUseCase
from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.user_factory import UserEntityFactoryInterface
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


# Application
def authenticate_user_uc_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
    password_hasher: PasswordHasherInterface = Depends(
        pwdlib_hasher_dependency
    ),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(
        user_repo=user_repo, password_hasher=password_hasher
    )


def register_user_uc_dependency(
    user_repo: UserRepositoryPort = Depends(in_memory_user_repository),
    user_factory: UserEntityFactoryInterface = Depends(
        user_entity_factory_dependency
    ),
    hasher: PasswordHasherInterface = Depends(pwdlib_hasher_dependency),
) -> RegisterUserUseCase:
    policies: list[PolicyInterface] = password_policies()
    return RegisterUserUseCase(
        user_repo=user_repo,
        user_factory=user_factory,
        hasher=hasher,
        policies=policies,
    )


# Presentation
def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserController:
    return RegisterUserController(use_case, logger)
