from application.dto.auth.jwt.auth_user import AuthUserDto
from application.ports.services.logger import LoggerPort
from application.use_cases.auth.registration.register import RegisterUserUseCase
from presentation.web.fastapi.schemas.request.auth.registration.login import (
    LoginUserRequestSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)
from presentation.web.fastapi.schemas.response.user.registered import (
    RegisteredUserResponseSchema,
)


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase, logger: LoggerPort):
        self._use_case = use_case
        self._logger = logger

    async def execute(
        self, body: LoginUserRequestSchema
    ) -> ItemResponseSchema[RegisteredUserResponseSchema]:
        self._logger.info(f"Registering user {body.email}")
        dto: AuthUserDto = await self._use_case.execute(
            email=body.email, password=body.password
        )
        user_response = RegisteredUserResponseSchema.model_validate(dto)
        self._logger.info(f"User {body.email} registered successfully")
        return ItemResponseSchema[RegisteredUserResponseSchema].build(
            data=user_response,
            status_code=201,
            message="UserEntity registered successfully",
        )
