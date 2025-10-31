from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from application.services.auth.jwt.facade import JwtAuthFacade


class LoginJwtController:
    def __init__(self, service: JwtAuthFacade):
        self.service = service

    def execute(self, email: str, password: str) -> JwtTokensOutDto:
        jwt_tokens: dict = self.service.login_user(email, password)
        return JwtTokensOutDto(**jwt_tokens)
