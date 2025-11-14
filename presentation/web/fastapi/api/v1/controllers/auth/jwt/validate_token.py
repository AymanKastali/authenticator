from application.dto.auth.jwt.claims import JwtClaimsDto
from application.ports.services.logger import LoggerPort
from application.use_cases.auth.jwt.validate_access_token import (
    ValidateAccessTokenUseCase,
)
from application.use_cases.auth.jwt.validate_refresh_token import (
    ValidateRefreshTokenUseCase,
)
from presentation.web.fastapi.schemas.request.auth.jwt.validate_token import (
    ValidateJwtTokenRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.claims import (
    JwtTokenClaimsResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class ValidateJwtTokenController:
    def __init__(
        self,
        validate_access_token: ValidateAccessTokenUseCase,
        validate_refresh_token: ValidateRefreshTokenUseCase,
        logger: LoggerPort,
    ):
        self._validate_access_token = validate_access_token
        self._validate_refresh_token = validate_refresh_token
        self._logger = logger

    async def execute(
        self, body: ValidateJwtTokenRequestSchema
    ) -> ItemResponseSchema[JwtTokenClaimsResponseSchema]:
        self._logger.info(
            f"[ValidateJwtTokenController] Verifying token for subject={body.subject}"
        )
        if body.token_type == "access":
            claims_dto: JwtClaimsDto = (
                await self._validate_access_token.execute(
                    body.token, body.subject
                )
            )
        else:
            claims_dto: JwtClaimsDto = (
                await self._validate_refresh_token.execute(body.token)
            )
        self._logger.info(
            f"[ValidateJwtTokenController] Token verification successful for subject={body.subject}"
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
