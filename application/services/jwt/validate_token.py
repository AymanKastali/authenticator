from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from application.services.jwt.jwt_blacklist import JwtBlacklistService
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity
from domain.factories.value_objects.uuid import UUIDVoFactory


class ValidateJwtTokenService:
    """
    Unified service to validate both access and refresh JWTs.
    Returns a JwtClaimsDto with is_valid=True if validation succeeds.
    """

    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        blacklist_service: JwtBlacklistService,
    ):
        self._validate_jwt = validate_jwt
        self._blacklist_service = blacklist_service

    async def execute(
        self, token: str, token_type: str, subject: str | None = None
    ) -> JwtClaimsDto:
        subject_vo = UUIDVoFactory.from_string(subject) if subject else None

        token_entity: JwtEntity = self._validate_jwt.execute(
            token=token, token_type=token_type, subject=subject_vo
        )
        await self._blacklist_service.assert_not_blacklisted(
            token_entity.claims.jti.value
        )

        claims_dict = JwtMapper.claims_to_dict(token_entity.claims)
        return JwtClaimsDto(**claims_dict)
