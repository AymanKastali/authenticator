from adapters.controllers.auth_controllers.jwt_refresh_token_controller import (
    JwtRefreshTokenController,
)
from adapters.dto.request_dto.refresh_jwt_token import RefreshJwtTokenDto
from adapters.dto.response_dto.jwt_response_model import (
    JwtResponseResponseModel,
)
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)


class JwtRefreshTokenHandler:
    def __init__(self, controller: JwtRefreshTokenController):
        self._controller = controller

    async def execute(
        self, body: RefreshJwtTokenDto
    ) -> ItemResponseModel[JwtResponseResponseModel]:
        jwt_tokens: JwtResponseResponseModel = self._controller.execute(
            token=body.refresh_token
        )
        return ItemResponseModel[JwtResponseResponseModel].build(
            data=jwt_tokens,
            status_code=200,
            message="JWT Token refreshed successfully",
        )
