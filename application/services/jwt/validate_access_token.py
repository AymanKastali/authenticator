from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from application.use_cases.jwt.assert_jwt_revocation import (
    AssertJwtRevocationUseCase,
)
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity
from domain.factories.value_objects.uuid import UUIDVoFactory


class ValidateJwtAccessTokenService:
    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        assert_jwt_revocation: AssertJwtRevocationUseCase,
    ):
        self._validate_jwt = validate_jwt
        self._assert_jwt_revocation = assert_jwt_revocation

    async def execute(
        self, token: str, subject: str | None = None
    ) -> JwtClaimsDto:
        subject_vo = UUIDVoFactory.from_string(subject) if subject else None
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token, subject_vo
        )
        await self._assert_jwt_revocation.execute(token_entity.uid)
        return JwtMapper.to_claims_dto_from_vo(token_entity.claims)
