from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.dto.request_dto.jwt_request_dto import RefreshJwtTokenInDto
from adapters.dto.response_dto.jwt_response_model import (
    JwtResponseResponseModel,
)
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)


class RefreshJwtTokenHandler:
    def __init__(self, controller: RefreshJwtTokenController):
        self._controller = controller

    async def execute(
        self, body: RefreshJwtTokenInDto
    ) -> ItemResponseModel[JwtResponseResponseModel]:
        jwt_tokens: JwtResponseResponseModel = self._controller.execute(
            token=body.refresh_token
        )
        return ItemResponseModel[JwtResponseResponseModel].build(
            data=jwt_tokens,
            status_code=200,
            message="JWT Token refreshed successfully",
        )
