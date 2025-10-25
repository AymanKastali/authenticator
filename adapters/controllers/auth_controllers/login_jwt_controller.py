from fastapi import HTTPException

from adapters.dto.response_dto.jwt_response_model import (
    JwtResponseResponseModel,
)
from application.services.jwt_auth_service import JwtAuthService


class JwtLoginController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    def execute(self, email: str, password: str) -> JwtResponseResponseModel:
        jwt_tokens: dict = self.service.execute(email, password)
        if not jwt_tokens:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JwtResponseResponseModel(**jwt_tokens)
