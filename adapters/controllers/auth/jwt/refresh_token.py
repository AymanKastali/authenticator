from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from application.dto.auth.jwt.tokens import JwtTokensDto
from application.services.auth.jwt.auth import JwtAuthService


class RefreshJwtTokenController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    async def execute(self, token: str) -> JwtTokensOutDto:
        jwt_tokens: JwtTokensDto = await self.service.refresh_jwt_token(token)
        return JwtTokensOutDto.model_validate(jwt_tokens)
