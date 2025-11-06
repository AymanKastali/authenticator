from application.dto.auth.jwt.token import JwtDto
from application.ports.services.logger import LoggerPort
from application.services.auth.jwt.auth import JwtAuthService
from presentation.web.fastapi.schemas.request.auth.jwt.verify_token import (
    VerifyJwtTokenRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.payload import (
    JwtTokenPayloadResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class VerifyJwtTokenController:
    def __init__(self, service: JwtAuthService, logger: LoggerPort):
        self._service = service
        self._logger = logger

    async def execute(
        self, body: VerifyJwtTokenRequestSchema
    ) -> ItemResponseSchema[JwtTokenPayloadResponseSchema]:
        self._logger.info(
            f"[VerifyJwtTokenController] Verifying token for subject={body.subject}"
        )
        dto: JwtDto = self._service.verify_jwt_token(body.token, body.subject)
        self._logger.info(
            f"[VerifyJwtTokenController] Token verification successful for subject={body.subject}"
        )
        payload = dto.payload
        payload_response = JwtTokenPayloadResponseSchema(
            user_id=payload.sub,
            token_type=payload.typ,
            expires_at=payload.exp,
            email=payload.email,
            username=payload.username,
            roles=payload.roles,
        )
        return ItemResponseSchema[JwtTokenPayloadResponseSchema].build(
            data=payload_response,
            status_code=200,
            message="JWT Token verified successfully",
        )
