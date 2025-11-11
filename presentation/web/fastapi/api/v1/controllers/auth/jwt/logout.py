from application.ports.services.logger import LoggerPort
from application.use_cases.auth.jwt.logout import LogoutUserUseCase
from presentation.web.fastapi.schemas.request.auth.jwt.logout import (
    LogoutJwtRequestSchema,
)


class JwtLogoutController:
    def __init__(self, logout_user: LogoutUserUseCase, logger: LoggerPort):
        self._logout_user = logout_user
        self._logger = logger

    async def execute(self, body: LogoutJwtRequestSchema) -> None:
        token = body.token

        self._logger.info(
            f"[JwtLogoutController] Attempting logout for token={token[:10]}"
        )
        await self._logout_user.execute(token)
        self._logger.info(
            f"[JwtLogoutController] Logout successful for token={token[:10]}"
        )
