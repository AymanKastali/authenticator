from adapters.controllers.auth.jwt.verify_token import (
    VerifyJwtTokenController,
)
from adapters.dto.request_dto.jwt_request_dto import VerifyJwtTokenInDto
from adapters.dto.response_dto.jwt_response_model import (
    JwtTokenPayloadOutDto,
)
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)


class VerifyJwtTokenHandler:
    def __init__(self, controller: VerifyJwtTokenController):
        self._controller = controller

    async def execute(
        self, body: VerifyJwtTokenInDto
    ) -> ItemResponseModel[JwtTokenPayloadOutDto]:
        jwt_token_payload_response_dto: JwtTokenPayloadOutDto = (
            self._controller.execute(body.token, body.subject)
        )
        return ItemResponseModel[JwtTokenPayloadOutDto].build(
            data=jwt_token_payload_response_dto,
            status_code=200,
            message="JWT Token verified successfully",
        )
