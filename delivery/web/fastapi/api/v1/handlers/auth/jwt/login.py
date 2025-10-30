from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.dto.requests.auth.registration.login import LoginUserInDto
from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from application.ports.services.logger import LoggerPort


class JwtLoginHandler:
    def __init__(self, controller: LoginJwtController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    async def execute(
        self, body: LoginUserInDto
    ) -> ItemOutDto[JwtTokensOutDto]:
        self._logger.info(
            f"[JwtLoginHandler] Attempting login for email={body.email}"
        )
        jwt_tokens: JwtTokensOutDto = self._controller.execute(
            email=body.email, password=body.password
        )
        self._logger.info(
            f"[JwtLoginHandler] Login successful for email={body.email}"
        )
        return ItemOutDto[JwtTokensOutDto].build(
            data=jwt_tokens, status_code=200, message="Login successful"
        )
