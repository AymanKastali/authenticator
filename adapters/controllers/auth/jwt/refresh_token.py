from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from application.services.auth.jwt.facade import JwtAuthFacade


class RefreshJwtTokenController:
    def __init__(self, service: JwtAuthFacade):
        self.service = service

    def execute(self, token: str) -> JwtTokensOutDto:
        jwt_tokens: dict = self.service.refresh_jwt_token(token)
        return JwtTokensOutDto(**jwt_tokens)
