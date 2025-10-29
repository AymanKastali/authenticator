from fastapi import HTTPException

from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from application.services.auth.jwt import JwtAuthService


class LoginJwtController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    def execute(self, email: str, password: str) -> JwtTokensOutDto:
        jwt_tokens: dict = self.service.login_user(email, password)
        if not jwt_tokens:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JwtTokensOutDto(**jwt_tokens)
