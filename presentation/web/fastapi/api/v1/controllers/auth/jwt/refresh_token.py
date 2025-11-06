from application.dto.auth.jwt.tokens import JwtTokensDto
from application.ports.services.logger import LoggerPort
from application.services.auth.jwt.auth import JwtAuthService
from presentation.web.fastapi.schemas.request.auth.jwt.refresh_token import (
    RefreshJwtTokenRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.tokens import (
    JwtTokensResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class RefreshJwtTokenController:
    def __init__(self, service: JwtAuthService, logger: LoggerPort):
        self._service = service
        self._logger = logger

    async def execute(
        self, body: RefreshJwtTokenRequestSchema
    ) -> ItemResponseSchema[JwtTokensResponseSchema]:
        self._logger.info(
            f"[RefreshJwtTokenController] Refreshing token: {body.refresh_token[:10]}***"
        )
        dto: JwtTokensDto = await self._service.refresh_jwt_token(
            body.refresh_token
        )
        jwt_tokens = JwtTokensResponseSchema.model_validate(dto)
        self._logger.info(
            "[RefreshJwtTokenController] Token refreshed successfully"
        )
        return ItemResponseSchema[JwtTokensResponseSchema].build(
            data=jwt_tokens,
            status_code=200,
            message="JWT Token refreshed successfully",
        )
