from application.dto.auth.jwt.auth_user import AuthUserDto
from application.ports.services.logger import LoggerPort
from application.use_cases.auth.register_user import (
    RegisterUserUseCase,
)
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
        email: str = str(body.email)
        password: str = body.password

        self._logger.info(f"Registering user {email}")
        dto: AuthUserDto = await self._use_case.execute(
            email=email, plain_password=password
        )
        user_response = RegisteredUserResponseSchema.model_validate(dto)
        self._logger.info(f"User {email} registered successfully")
        return ItemResponseSchema[RegisteredUserResponseSchema].build(
            data=user_response,
            status_code=201,
            message="UserEntity registered successfully",
        )
