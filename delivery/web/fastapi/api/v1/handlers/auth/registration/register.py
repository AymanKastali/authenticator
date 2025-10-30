from adapters.controllers.auth.registration.register import (
    RegisterUserController,
)
from adapters.dto.requests.auth.registration.login import LoginUserInDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.user.registered import RegisteredUserOutDto
from application.ports.services.logger import LoggerPort


class RegisterUserHandler:
    def __init__(self, controller: RegisterUserController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    async def execute(
        self, body: LoginUserInDto
    ) -> ItemOutDto[RegisteredUserOutDto]:
        self._logger.info(f"Registering user {body.email}")
        user: RegisteredUserOutDto = self._controller.execute(
            email=body.email, password=body.password
        )
        self._logger.info(f"User {body.email} registered successfully")
        return ItemOutDto[RegisteredUserOutDto].build(
            data=user,
            status_code=201,
            message="UserEntity registered successfully",
        )
