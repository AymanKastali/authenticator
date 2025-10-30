from adapters.controllers.auth.jwt.verify_token import VerifyJwtTokenController
from adapters.dto.requests.auth.jwt.verify_token import VerifyJwtTokenInDto
from adapters.dto.responses.auth.jwt.payload import JwtTokenPayloadOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from application.ports.services.logger import LoggerPort


class VerifyJwtTokenHandler:
    def __init__(
        self, controller: VerifyJwtTokenController, logger: LoggerPort
    ):
        self._controller = controller
        self._logger = logger

    async def execute(
        self, body: VerifyJwtTokenInDto
    ) -> ItemOutDto[JwtTokenPayloadOutDto]:
        self._logger.info(
            f"[VerifyJwtTokenHandler] Verifying token for subject={body.subject}"
        )
        jwt_token_payload_response_dto: JwtTokenPayloadOutDto = (
            self._controller.execute(body.token, body.subject)
        )
        self._logger.info(
            f"[VerifyJwtTokenHandler] Token verification successful for subject={body.subject}"
        )
        return ItemOutDto[JwtTokenPayloadOutDto].build(
            data=jwt_token_payload_response_dto,
            status_code=200,
            message="JWT Token verified successfully",
        )
