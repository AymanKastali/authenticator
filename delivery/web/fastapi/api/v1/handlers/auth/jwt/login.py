from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.dto.requests.auth.registration.login import LoginUserInDto
from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto


class JwtLoginHandler:
    def __init__(self, controller: LoginJwtController):
        self._controller = controller

    async def execute(
        self, body: LoginUserInDto
    ) -> ItemOutDto[JwtTokensOutDto]:
        jwt_tokens: JwtTokensOutDto = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemOutDto[JwtTokensOutDto].build(
            data=jwt_tokens, status_code=200, message="Login successful"
        )
