from adapters.controllers.auth.jwt.logout import LogoutJwtController
from adapters.dto.requests.auth.jwt.logout import LogoutJwtInDto
from application.ports.services.logger import LoggerPort


class JwtLogoutHandler:
    def __init__(self, controller: LogoutJwtController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    async def execute(self, body: LogoutJwtInDto) -> None:
        token = body.token

        self._logger.info(
            f"[JwtLogoutHandler] Attempting logout for token={token[:10]}"
        )
        await self._controller.execute(token)
        self._logger.info(
            f"[JwtLogoutHandler] Logout successful for token={token[:10]}"
        )
