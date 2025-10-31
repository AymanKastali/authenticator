from adapters.dto.responses.auth.jwt.payload import JwtTokenPayloadOutDto
from application.dto.auth.jwt.token import JwtDto
from application.services.auth.jwt.facade import JwtAuthFacade


class VerifyJwtTokenController:
    def __init__(self, service: JwtAuthFacade):
        self.service = service

    def execute(
        self, token: str, subject: str | None = None
    ) -> JwtTokenPayloadOutDto:
        token_dto: JwtDto = self.service.verify_jwt_token(token, subject)
        payload_dto = token_dto.payload
        jwt_token_payload_response_dto = JwtTokenPayloadOutDto(
            user_id=payload_dto.sub,
            token_type=payload_dto.typ,
            expires_at=payload_dto.exp,
            email=payload_dto.email,
            username=payload_dto.username,
            roles=payload_dto.roles,
        )
        return jwt_token_payload_response_dto
