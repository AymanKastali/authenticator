from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.dto.requests.auth.jwt.refresh_token import RefreshJwtTokenInDto
from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from application.ports.services.logger import LoggerPort


class RefreshJwtTokenHandler:
    def __init__(
        self, controller: RefreshJwtTokenController, logger: LoggerPort
    ):
        self._controller = controller
        self._logger = logger

    async def execute(
        self, body: RefreshJwtTokenInDto
    ) -> ItemOutDto[JwtTokensOutDto]:
        self._logger.info(
            f"[RefreshJwtTokenHandler] Refreshing token: {body.refresh_token[:10]}***"
        )
        jwt_tokens: JwtTokensOutDto = self._controller.execute(
            token=body.refresh_token
        )
        self._logger.info(
            "[RefreshJwtTokenHandler] Token refreshed successfully"
        )
        return ItemOutDto[JwtTokensOutDto].build(
            data=jwt_tokens,
            status_code=200,
            message="JWT Token refreshed successfully",
        )
