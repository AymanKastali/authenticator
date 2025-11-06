from application.ports.services.logger import LoggerPort
from application.services.auth.jwt.auth import JwtAuthService
from presentation.web.fastapi.schemas.request.auth.jwt.logout import (
    LogoutJwtRequestSchema,
)


class JwtLogoutController:
    def __init__(self, service: JwtAuthService, logger: LoggerPort):
        self._service = service
        self._logger = logger

    async def execute(self, body: LogoutJwtRequestSchema) -> None:
        token = body.token

        self._logger.info(
            f"[JwtLogoutController] Attempting logout for token={token[:10]}"
        )
        await self._service.logout(token)
        self._logger.info(
            f"[JwtLogoutController] Logout successful for token={token[:10]}"
        )
