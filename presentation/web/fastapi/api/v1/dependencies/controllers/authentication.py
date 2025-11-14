from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.auth.register.register_user import (
    RegisterUserUseCase,
)
from presentation.web.fastapi.api.v1.controllers.auth.registration.register import (
    RegisterUserController,
)
from presentation.web.fastapi.api.v1.dependencies.application.authientication import (
    register_user_uc_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.logger import (
    get_console_json_logger,
)


def register_user_controller_dependency(
    use_case: RegisterUserUseCase = Depends(register_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RegisterUserController:
    return RegisterUserController(use_case, logger)
