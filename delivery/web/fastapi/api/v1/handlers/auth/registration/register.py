from adapters.controllers.auth.registration.register import (
    RegisterUserController,
)
from adapters.dto.requests.auth.registration.login import LoginUserInDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.user.registered import RegisteredUserOutDto


class RegisterUserHandler:
    def __init__(self, controller: RegisterUserController):
        self._controller = controller

    async def execute(
        self, body: LoginUserInDto
    ) -> ItemOutDto[RegisteredUserOutDto]:
        user: RegisteredUserOutDto = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemOutDto[RegisteredUserOutDto].build(
            data=user,
            status_code=201,
            message="UserEntity registered successfully",
        )
