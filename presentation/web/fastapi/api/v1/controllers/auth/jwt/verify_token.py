from application.dto.auth.jwt.claims import JwtClaimsDto
from application.ports.services.logger import LoggerPort
from application.use_cases.auth.jwt.verify_access_token import (
    VerifyAccessTokenUseCase,
)
from presentation.web.fastapi.schemas.request.auth.jwt.verify_token import (
    VerifyJwtTokenRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.claims import (
    JwtTokenClaimsResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class VerifyJwtTokenController:
    def __init__(
        self, verify_access_token: VerifyAccessTokenUseCase, logger: LoggerPort
    ):
        self._verify_access_token = verify_access_token
        self._logger = logger

    async def execute(
        self, body: VerifyJwtTokenRequestSchema
    ) -> ItemResponseSchema[JwtTokenClaimsResponseSchema]:
        self._logger.info(
            f"[VerifyJwtTokenController] Verifying token for subject={body.subject}"
        )
        claims_dto: JwtClaimsDto = await self._verify_access_token.execute(
            body.token, body.subject
        )
        self._logger.info(
            f"[VerifyJwtTokenController] Token verification successful for subject={body.subject}"
        )
        claims_response = JwtTokenClaimsResponseSchema(
            user_id=claims_dto.sub,
            token_type=claims_dto.typ,
            expires_at=claims_dto.exp,
            email=claims_dto.email,
            username=claims_dto.username,
            roles=claims_dto.roles,
        )
        return ItemResponseSchema[JwtTokenClaimsResponseSchema].build(
            data=claims_response,
            status_code=200,
            message="JWT Token verified successfully",
        )
