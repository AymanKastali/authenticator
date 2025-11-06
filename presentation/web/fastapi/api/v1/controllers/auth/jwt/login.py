from application.dto.auth.jwt.tokens import JwtTokensDto
from application.ports.services.logger import LoggerPort
from application.services.auth.jwt.auth import JwtAuthService
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
    def __init__(self, service: JwtAuthService, logger: LoggerPort):
        self._service = service
        self._logger = logger

    async def execute(
        self, body: LoginUserRequestSchema
    ) -> ItemResponseSchema[JwtTokensResponseSchema]:
        self._logger.info(
            f"[JwtLoginController] Attempting login for email={body.email}"
        )
        dto: JwtTokensDto = await self._service.login(
            email=body.email, password=body.password
        )
        jwt_tokens = JwtTokensResponseSchema.model_validate(dto)
        self._logger.info(
            f"[JwtLoginController] Login successful for email={body.email}"
        )
        return ItemResponseSchema[JwtTokensResponseSchema].build(
            data=jwt_tokens, status_code=200, message="Login successful"
        )
