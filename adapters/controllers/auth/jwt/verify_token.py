from adapters.dto.responses.auth.jwt.payload import JwtTokenPayloadOutDto
from application.dto.auth.jwt.token import JwtTokenPayloadDto
from application.services.auth.jwt import JwtAuthService


class VerifyJwtTokenController:
    def __init__(self, service: JwtAuthService):
        self.service = service

    def execute(
        self, token: str, subject: str | None = None
    ) -> JwtTokenPayloadOutDto:
        jwt_token_payload_dto: JwtTokenPayloadDto = (
            self.service.verify_jwt_token(token, subject)
        )
        jwt_token_payload_response_dto = JwtTokenPayloadOutDto(
            user_id=jwt_token_payload_dto.sub,
            token_type=jwt_token_payload_dto.typ,
            expires_at=jwt_token_payload_dto.exp,
            email=jwt_token_payload_dto.email,
            username=jwt_token_payload_dto.username,
            roles=jwt_token_payload_dto.roles,
        )
        return jwt_token_payload_response_dto
