from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from application.services.auth.jwt.auth import JwtAuthService


class LoginJwtController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    async def execute(self, email: str, password: str) -> JwtTokensOutDto:
        jwt_tokens: dict = await self.service.login(email, password)
        return JwtTokensOutDto(**jwt_tokens)
