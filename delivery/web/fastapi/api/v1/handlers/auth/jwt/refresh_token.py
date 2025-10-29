from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.dto.requests.auth.jwt.refresh_token import RefreshJwtTokenInDto
from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto


class RefreshJwtTokenHandler:
    def __init__(self, controller: RefreshJwtTokenController):
        self._controller = controller

    async def execute(
        self, body: RefreshJwtTokenInDto
    ) -> ItemOutDto[JwtTokensOutDto]:
        jwt_tokens: JwtTokensOutDto = self._controller.execute(
            token=body.refresh_token
        )
        return ItemOutDto[JwtTokensOutDto].build(
            data=jwt_tokens,
            status_code=200,
            message="JWT Token refreshed successfully",
        )
