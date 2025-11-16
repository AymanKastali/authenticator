from application.ports.services.logger import LoggerPort
from application.services.jwt.logout import JwtLogoutUserService
from presentation.web.fastapi.schemas.request.auth.jwt.logout import (
    LogoutJwtRequestSchema,
)


class JwtLogoutController:
    def __init__(self, service: JwtLogoutUserService, logger: LoggerPort):
        self._service = service
        self._logger = logger

    async def execute(self, body: LogoutJwtRequestSchema) -> None:
        token = body.token

        self._logger.info(
            f"[JwtLogoutController] Attempting logout for token={token[:10]}"
        )
        await self._service.execute(token)
        self._logger.info(
            f"[JwtLogoutController] Logout successful for token={token[:10]}"
        )
