from adapters.dto.response_dto.jwt_response_model import (
    JwtResponseResponseModel,
)
from application.services.jwt_auth_service import JwtAuthService


class RefreshJwtTokenController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    def execute(self, token: str) -> JwtResponseResponseModel:
        jwt_tokens: dict = self.service.refresh_jwt_token(token)
        return JwtResponseResponseModel(**jwt_tokens)
