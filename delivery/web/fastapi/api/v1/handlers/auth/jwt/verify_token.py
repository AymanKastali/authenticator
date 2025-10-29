from adapters.controllers.auth.jwt.verify_token import VerifyJwtTokenController
from adapters.dto.requests.auth.jwt.verify_token import VerifyJwtTokenInDto
from adapters.dto.responses.auth.jwt.payload import JwtTokenPayloadOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto


class VerifyJwtTokenHandler:
    def __init__(self, controller: VerifyJwtTokenController):
        self._controller = controller

    async def execute(
        self, body: VerifyJwtTokenInDto
    ) -> ItemOutDto[JwtTokenPayloadOutDto]:
        jwt_token_payload_response_dto: JwtTokenPayloadOutDto = (
            self._controller.execute(body.token, body.subject)
        )
        return ItemOutDto[JwtTokenPayloadOutDto].build(
            data=jwt_token_payload_response_dto,
            status_code=200,
            message="JWT Token verified successfully",
        )
