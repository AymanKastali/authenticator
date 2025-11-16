from application.ports.services.logger import LoggerPort
from application.services.jwt.login import JwtLoginUserService
from presentation.web.fastapi.schemas.request.auth.registration.login import (
    LoginUserRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.tokens import (
    JwtTokensResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class JwtLoginController:
    def __init__(self, login_user: JwtLoginUserService, logger: LoggerPort):
        self._login_user = login_user
        self._logger = logger

    async def execute(self, body: LoginUserRequestSchema):
        self._logger.info(f"Attempting login for email={body.email}")
        dto = await self._login_user.execute(body.email, body.password)
        self._logger.info(f"Login successful for email={body.email}")
        return ItemResponseSchema[JwtTokensResponseSchema].build(
            data=JwtTokensResponseSchema.model_validate(dto),
            status_code=200,
            message="Login successful",
        )
